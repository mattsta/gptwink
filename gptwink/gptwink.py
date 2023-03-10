from __future__ import annotations

import orjson
import aiohttp
import asyncio
from aiohttp_sse_client import client as sse_client  # type: ignore

from loguru import logger
from typing import Literal, TypeAlias, Final, Iterator

import ulid
import pathlib
from dataclasses import dataclass, field

# Name some ugly types for multiple reuse
Role: TypeAlias = Literal["system", "user", "assistant"]
RoleContent: TypeAlias = list[tuple[Role, str]]
Usage: TypeAlias = dict[str, int]
Choice: TypeAlias = dict[str, str]
Choices: TypeAlias = list[dict[str, str | int | Choice]]
APIArgs: TypeAlias = str | int | float | list[str]
APIArgsSaved: TypeAlias = dict[str, APIArgs]


@dataclass
class GPTwink:
    """Un-Garbage Chapht API.

    ref: https://platform.openai.com/docs/api-reference/chat
    """

    # BYO-Key
    key: str = field(repr=False)

    # BYO-Session
    session: aiohttp.ClientSession

    # api config options
    model: str = "gpt-3.5-turbo"
    temp: float = 1
    top_p: float = 1

    stream: bool = True
    user: str = "Chöd"

    api: Final = "https://api.openai.com/v1/chat/completions"

    def __post_init__(self) -> None:
        assert self.key.startswith("sk-")
        self.auth = dict(Authorization=f"Bearer {self.key}")

    def build(self, rc: list[tuple[str, str]]) -> RoleContent:
        """Convert any role+content shorthand to official format."""
        send: RoleContent = []
        for r, c in rc:
            match r.lower()[0]:
                case "s":
                    # motivation / "stage directions"
                    send.append(("system", c))
                case "a":
                    # responses from upstream
                    send.append(("assistant", c))
                case "u":
                    # input to the model's confabulator
                    send.append(("user", c))

        return send

    async def chat(self, rc: RoleContent, **apiargs: APIArgs) -> Answer:
        """Send request to API.

        'rc' is the [(role, content)] mapping: https://platform.openai.com/docs/guides/chat
        'apiargs' is a dict of optional API arguments
        """

        formatted = [dict(role=role, content=content) for role, content in rc]
        req = dict(model=self.model, messages=formatted)

        # "stream" implies live console output for now. This could technically take a better
        # callback mechanism, but we're rapidly iterating here.
        if self.stream:
            # So this technically works, but it:
            #  - doesn't include the regular metadata for usage (even at the end), so
            #    we can't keep our "used tokens" counter running.
            #  - It also doesn't generate the regular formats we expect, so if we use this,
            #    we have to accumulate the results in a kinda ugly way which breaks our
            #    abstraction layers...
            async with sse_client.EventSource(
                self.api,
                dict(method="POST"),  # required
                session=self.session,
                json=req | apiargs | dict(stream=True),
                headers=self.auth,
            ) as es:
                try:
                    tokcount = 0
                    toks: list[str] = []
                    async for ev in es:
                        # logger.info("msg: {}", ev)
                        if ev.data == "[DONE]":
                            # yer done!
                            # it's so nice of thier API to make the field JSON _except_ for the final message,
                            # so we can't just always parse the field. good job everybody.
                            print("\n")
                            answerstream = dict(
                                usage=dict(stream_generated_tokens=tokcount),
                                choices=[
                                    dict(
                                        message=dict(
                                            role="assistant", content="".join(toks)
                                        )
                                    )
                                ],
                            )
                            return Answer(self, answerstream, rc, apiargs)  # type: ignore

                        # 'ev' looks something like:
                        # MessageEvent(type=None, message='', data='{"id":"chatcmpl-XXXXXXXXXXXXX","object":"chat.completion.chunk","created":1678162501,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"role":"assistant"},"index":0,"finish_reason":null}]}', origin='https://api.openai.com', last_event_id='')
                        # MessageEvent(type=None, message='', data='{"id":"chatcmpl-XXXXXXXXXXXXX","object":"chat.completion.chunk","created":1678161812,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"Lorem"},"index":0,"finish_reason":null}]}', origin='https://api.openai.com', last_event_id='')
                        data = orjson.loads(ev.data)
                        # lovely data format (vomit)
                        token = data["choices"][0]["delta"].get("content")

                        if token:
                            # we're hacking the print here because we want it "live"
                            if tokcount == 0:
                                print("assistant> ", end="", flush=True)

                            tokcount += 1
                            toks.append(token)
                            print(token, end="", flush=True)
                except:
                    logger.warning("Connection error?")

                # TODO: Better error handling here for the streaming case
                assert None, "Message didn't end? Not enough tokens?"

        async with self.session.post(
            self.api, json=req | apiargs, headers=self.auth
        ) as got:
            answer = await got.json()

            return Answer(self, answer, rc, apiargs)

    async def again(self, previous: Answer, rc: RoleContent) -> Answer:
        """Extend current prompt with new output appended."""

        # run query again but add next content block...
        return await self.chat(previous.rc + rc, **previous.args)


@dataclass
class Answer:
    """Represents the response to a chat input."""

    gpt: GPTwink

    # answer results from upstream
    answer: dict[str, str | int | Usage | Choices]

    # input to this answer
    rc: RoleContent

    # any special args provided from the request
    args: APIArgsSaved

    def usage(self) -> Usage:
        return self.answer["usage"]  # type: ignore

    def messages(self) -> Iterator[Choice]:
        """Return messages from the API result.

        The API currently only returns 1 message, but maybe..."""

        # "choices" only exists if the output was generated.
        # If output fails (too many tokens, etc) there will be just
        # {"error": {"message": U SUCK}} instead
        for choice in self.answer.get("choices", dict(message=[])):  # type: ignore
            # these are implicitly of "role==assistant"
            yield choice["message"]  # type: ignore

    async def again(self, rc: RoleContent | None = None) -> Answer | None:
        """Run a request by appending new 'rc' to already-generated output."""

        # current output for adding to previous output
        send: RoleContent = [(m["role"], m["content"]) for m in self.messages()]  # type: ignore

        # if no previous message, something broke (out of tokens?) and we can't continue.
        if not send:
            return None

        if rc:
            # append optional additional input to previous input
            send += rc

        # generate next output
        return await self.gpt.again(self, send)


@dataclass
class Agent:
    """One instance of a Salon attendee"""

    name: str
    gpt: GPTwink
    system: str
    save: pathlib.Path

    previous: Answer | None = None

    def __post_init__(self) -> None:
        self.save.mkdir(parents=True, exist_ok=True)

    async def setup(self) -> Answer:
        self.previous = await self.gpt.chat([("system", self.system)])
        return self.previous

    async def again(self, peers: RoleContent | None = None) -> Answer | None:
        if not self.previous:
            return None

        self.previous = await self.previous.again(peers)
        return self.previous


@dataclass
class Salon:
    """what if we share outputs between motivators?"""

    # give this room a name for saving results...
    name: str

    gpt: GPTwink

    # provide a list of system prompts; each list element will generate a new mind instance.
    # Format is: (name of agent, startup directions for agent)
    systems: list[tuple[str, str]]

    # number of times everything can chat between everything else
    max_steps: int = 32

    def __post_init__(self) -> None:
        # Save outputs here:
        start = pathlib.Path(self.name) / str(ulid.new())

        self.agents: list[Agent] = []
        for agentname, prompt in self.systems:
            adir = start / agentname
            self.agents.append(Agent(agentname, self.gpt, prompt, adir))

    async def start(self) -> None:
        # Initialize each agent with its custom system prompt
        agents = await asyncio.gather(*[a.setup() for a in self.agents])

        # TODO: save results, add by name, then append to peers NOT your own name.
        # TODO: save each output flow to text files
        # TODO: find a good print format for everything at once

        # run all agents, collect all output, append all output to all agents, repeat
        family = None
        for _ in range(self.max_steps):
            await asyncio.gather(*[agent.again(family) for agent in agents])
            family = ...


def chatCLI(stream: bool = True) -> None:
    """Self-service chat UI"""
    import dotenv
    import sys
    import os

    from prompt_toolkit import PromptSession
    from prompt_toolkit.application import get_app
    from prompt_toolkit.shortcuts import set_title
    from prompt_toolkit import prompt
    from prompt_toolkit.formatted_text import HTML

    CONFIG = {**dotenv.dotenv_values(".env.gptwink"), **os.environ}

    set_title("GPTwink GPT GPT GPT GPT")

    try:
        KEY = CONFIG["OPENAI_API_KEY"]
    except:
        logger.error("wut bruv, ya need yer aayyyy peee eye key yah")
        sys.exit(1)

    def status(got: Answer | None) -> HTML:
        return HTML(got.answer.get("usage", "No usage calcualted when streaming...") if got else "No status yet?")  # type: ignore

    @logger.catch()
    async def looper() -> None:
        session = PromptSession()  # type: ignore
        app = session.app

        async with aiohttp.ClientSession() as client:
            assert KEY
            gpt = GPTwink(KEY, client)
            while True:
                try:
                    i = await session.prompt_async(
                        "system> ", bottom_toolbar=f"Ready for first request..."
                    )

                    if not i.strip():
                        continue

                    got: Answer | None = await gpt.chat([("system", i)])
                    break

                    assert got
                    print("assistant>", *[m["content"] for m in got.messages()])
                except EOFError:
                    logger.warning("Goodbye for now! You didn't even do anything!")
                    return
                except KeyboardInterrupt:
                    pass
                except:
                    logger.exception("come again?")

            while True:
                try:
                    i = await session.prompt_async("user> ", bottom_toolbar=status(got))

                    # ignore empty lines
                    if not i.strip():
                        continue

                    assert got
                    got = await got.again([("user", i)])

                    if not got:
                        print("No current session has no remaining contunity! Failing.")
                        return

                    # only print full result of not "live / streaming" because if we streamed
                    # the result, we printed the live output in the network loop.
                    if not got.gpt.stream:
                        print(
                            "\nassistant>",
                            *[m["content"] for m in got.messages()],
                            "\n",
                        )
                except EOFError:
                    logger.warning("Goodbye for now!")
                    return
                except KeyboardInterrupt:
                    pass
                except:
                    logger.exception("what now?")

    asyncio.run(looper())


def cmd() -> None:
    import fire

    fire.Fire(chatCLI)


if __name__ == "__main__":
    cmd()
