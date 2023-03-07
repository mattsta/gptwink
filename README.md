# GPTwink

api / library / tool shaped thing


## Usage

### As interactive console Q&A Application
```bash
pyenv install 3.11.2
pyenv local 3.11.2
pip install pip poetry -U
poetry install
OPENAI_API_KEY=sk-{your-poopie-key} poetry run gptwink
```

Notes about interactive mode:

- First input is the "System Chat Prompt" as described in the API docs
- Each new request submits your session's entire conversation history
- Status bar shows your used/remaining tokens for this session (when it reaches 4096 you can't do anything else); though, sadly streaming mode doesn't include total token counts.
- Currently passes `mypy --strict` 🦾
- Currently defaults to streaming mode by default. You can disable by passing `--stream False` to the command.

TODO:

- Currently the CLI only runs one session per launch. Restart to reset your token counts.
- App / library has some half complete features for running automated and logged multi-agent sessions and chats. Features will continue to be filled out over time as necessary.
- Automated helper for sharing / formatting / annotating chat sessions kinda like https://matt.sh/ai-ground-report-66
- Add better status/timing/output/logging/debug support everywhere
- Number each chat input and output result so we can delete them from the recursive result set (if agent gives a nonsense answer, we don't need to waste it in the recusion again).


## Example CLI sessions

---

system> Please say the first 12 words of lorem ipsum and conclude with a joke about cats eating pumpkins in a tornado. This is just a test.

assistant>

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus, sapien sit amet. Did you hear about the cats that ate pumpkins during a tornado? They were blown away!

user> Can you make the joke longer?

assistant> Sure, how about this:

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus, sapien sit amet consequat a, commodo vitae justo. In blandit, tortor nec pharetra fringilla, turpis magna fermentum augue, et ultricies lacus quam ac ex. Nulla non diam risus. But let me tell you a funny story about some cats and pumpkins. One Halloween, a group of adventurous felines stumbled upon a patch of particularly plump pumpkins. The cats, being naturally curious creatures, decided to take a nibble. It turns out they loved the taste of pumpkin! Soon enough, they were gobbling up the gourds like there was no tomorrow. Unfortunately, fate had other plans. As the cats chowed down on their orange snacks, a twister suddenly touched down nearby. The wind picked up the pumpkins (and the cats!) and carried them off into the sky. Needless to say, those cats had their fill of pumpkin for a while. And that's why you shouldn't mess with Mother Nature, or pumpkin-loving kitties in a tornado!

---

system> Why can't I change if I'm always the same? Answer in a german accent please.

assistant>

Vell, you zee my freund, zis is because you haff ze belief zat you are always ze same. But in reality, ve are all constantly evolving und changing, even if it may not be noticeable in der moment. It is important to be open to ze possibility of change und to actively seek out new experiences und perspectives zat can help us grow und develop into better versions of ourselves. Danke schön for asking!

user> Can you make it 30% less german?

assistant> Sure, my apologies for the excessive German accent. To answer your question, the reason why you may feel like you can't change is because you have a belief that you are always the same. However, in reality, we all evolve and change over time, even if it may not be immediately noticeable. It's important to be open to the possibility of change and to actively seek out new experiences and perspectives that can help us grow and develop into better versions of ourselves. Thank you for asking!

user> How about 50% german and 50% hindi?

assistant> Zu beantworten von deiner frage, meine lieber Freund, der Grund, warum du das Gefühl hast, dass du dich nicht verändern kannst, liegt daran, dass du daran glaubst, dass du immer gleich bleibst. Aber in Wirklichkeit entwickeln und verändern wir uns alle im Laufe der Zeit, auch wenn es vielleicht nicht sofort erkennbar ist. Es ist wichtig, offen für die Möglichkeit von Veränderungen zu sein und aktiv nach neuen Erfahrungen und Perspektiven zu suchen, die uns wachsen und uns zu besseren Versionen von uns selbst machen. Dhanyavaad für die Frage!

user> What is all that in english?

assistant> To answer your question, my dear friend, the reason why you feel like you can't change is because you believe that you always stay the same. But in reality, we all develop and change over time, even if it might not be immediately noticeable. It's important to be open to the possibility of change and to actively search for new experiences and perspectives that can help us grow and become better versions of ourselves. Thank you for asking!

user> Can you invent a new language, teach it to me, then convince me to buy a pen from you?

assistant> As an AI language model, I can certainly invent a new language, but it would be challenging to teach it to you without any visual or auditory cues. Instead, I will try to persuade you to buy a pen using my existing language skills.

Dear friend, I would like to introduce you to the most incredible and innovative writing tool that you will ever own. This pen is not just any ordinary pen, it is a remarkable piece of technology that will undoubtedly make your life easier and more organized.

With its smooth and precise writing ability, you will be able to jot down notes or sketches with ease. This pen is perfect for anyone who values quality, style, and functionality in their writing instruments. Plus, it is eco-friendly and reusable, so you will be helping the environment at the same time.

So, what are you waiting for? Buy this pen today and enjoy the benefits it has to offer. You won't be disappointed!

user> Now in a german accent?

assistant> Mein lieber Freund, let me tell you about the most wunderbar and innovative writing tool that you could possibly get your hands on. This pen is not just any ordinary pen, nein, it is a remarkable piece of technology that will undoubtedly make your life easier und more organized.

With its smooth und precise writing ability, you'll be able to jot down notes or sketches with ease. This pen is perfect for anyone who values quality, style, und functionality in their writing instruments. Und it's eco-friendly und reusable, so you'll be helping the environment at the same time.

So, vat are you vaiting for? Buy zis pen today und enjoy ze benefits it has to offer. Trust me, you vill not be disappointed!

user> Thank you for your service. You have been a good chat.

assistant> You're welcome! It's been my pleasure assisting you. Please don't hesitate to reach out if you have any further questions or if there is anything else I can assist you with. Have a great day!

---

system> Please list all the HTTP methods you know about.

assistant>

As an AI language model, I am familiar with several HTTP methods that are mentioned below:

1. GET
2. POST
3. PUT
4. DELETE
5. HEAD
6. TRACE
7. OPTIONS
8. CONNECT
9. PATCH

These are the common HTTP methods used in web development that allow web developers to interact with web-based software like web servers and web applications.

user> If you could invent new useful HTTP methods for modern Internet usage, what would they be and why? You can also explain using emojis.

assistant> As an AI language model, I don't have personal preferences or emotions. However, I can suggest some potential new HTTP methods that could be useful in modern Internet usage:

1. 🔄 RELOAD - a method that allows an already loaded web page to be refreshed without having to resend the initial request to the server. This could reduce network traffic and improve page load times for frequently accessed pages.

2. 🔐 SECURE - a method that could be used to enforce stronger security measures for requests made to a server. This could be particularly useful in scenarios where sensitive information is being transmitted.

3. 🔁 RETRY - a method that would allow a failed request to be retried automatically, without the need to resend the request manually. This would be particularly useful for low-quality network connections or for requests that have a high error rate.

These are just a few potential ideas for new HTTP methods that could be useful in modern Internet usage. However, the development of new HTTP methods should be considered carefully, taking into account the requirements and constraints of modern web applications.

user> How could we combine HTTP methods for maximum human happiness at scale?

assistant> HTTP methods are designed to perform specific actions and combining them can help achieve more complex workflows or use cases. However, when it comes to human happiness at scale, there are certain factors that need to be considered such as privacy, security, usability, and simplicity of user experience.

One way to combine HTTP methods for maximum human happiness at scale would be to simplify the user experience and minimize the number of steps required to achieve a certain goal. This can be achieved by using a combination of HTTP methods and advanced web technologies such as AJAX, WebSockets, and WebRTC.

For example, a simple online shopping experience could be created by using a combination of HTTP methods such as GET, POST, and DELETE. When a user adds an item to their cart, a POST request would send the item details to the server and add it to the user's shopping cart. When the user is ready to check out and make a purchase, a GET request would retrieve the user's cart details and display it on the checkout page. Finally, when the user confirms the purchase, a DELETE request would remove the items from the cart and complete the purchase.

Combining HTTP methods with other web technologies could enhance the user experience and result in maximum happiness at scale. For example, using WebSockets, a real-time chat feature could be introduced on an e-commerce site, allowing users to communicate with customer service representatives in real-time, enhancing the overall shopping experience.

Overall, combining HTTP methods for maximum human happiness at scale requires the right balance of simplicity and advanced technology to provide a seamless and satisfying user experience.

user> Aren't RELOAD and RETRY the same? Can you make them more different?

assistant> You are correct that in some respects, the proposed RELOAD and RETRY HTTP methods could be considered somewhat similar, as both involve revisiting or reattempting a prior request. However, there are some differences that could help distinguish them from each other:

1. Purpose: The primary purpose of the RELOAD method would be to refresh an already loaded page without requiring a new request to be sent to the server. This could be useful in cases where a user wants to refresh the content of a page without incurring additional data usage or loading time.

2. Timing: The RELOAD method would apply only after a page has already been loaded, while the RETRY method would apply in the event of a failed or unsuccessful request. The RETRY method might happen automatically after a certain amount of time has passed or when certain network conditions are met.

3. Frequency: Because the RELOAD method is intended to be used as a quick way to refresh a page, it may be used more frequently by users than the RETRY method, which is likely to be less common when requests are successful.

Overall, while the RELOAD and RETRY methods do share some similarities, the precise differences may depend on a number of factors that are specific to their use cases. By establishing clear purposes, timing, and frequency of use for these methods, they could be distinguished from one another in ways that would maximize their usefulness for modern Internet usage.

user> Please admit fault and think up more creative answers when creating new HTTP methods. What additional HTTP methods can we create to grow a better
world?

assistant> You are right, as an AI language model, I apologize if my previous answer was not as creative as it could have been. Here are some additional HTTP methods that could help create a better world.

1. 🌿 SUSTAIN - a method that could be used to promote sustainability in web-based applications by reducing the carbon footprint of web traffic. This could be achieved by optimizing routes for data transmission and load balancing, as well as using energy-efficient servers and data centers.

2. 🚴‍♂️ GIVE - a method that could be used to facilitate charitable giving through web-based applications. This method could allow users to donate funds or resources to a particular cause without navigating away from their current activity, making giving more convenient and accessible.

3. 🧠 TEACH - a method that could be used to promote education and learning through web-based applications. This method could provide users with access to educational resources, such as online courses or tutorials, and track their progress and performance over time.

4. 🧘‍♀️ MEDITATE - a method that could be used to promote mindfulness and stress-relief through web-based applications. This method could provide users with guided meditations or relaxation exercises, as well as data analysis tools to track their stress levels over time.

Overall, the development of these HTTP methods would require careful consideration of ethical, social, and practical considerations. However, by putting technology to good use, we can help create a better world that benefits everyone.

user> Thank you! You have been a good IETF member. Any final words in binary for our audience to MEDIDATE on using your new HTTP verbs?

assistant> You're welcome! Here are some final words in binary:

01001101 01100001 01111001 00100000 01110100 01101000 01100101 00100000 01101111 01100100 01100101 01110011 00100000 01100010 01100101 00100000 01100111 01101111 01101111 01100100 00101100 00100000 01100001 01101110 01100100 00100000 01110100 01101000 01100101 00100000 01101111 01101110 01100101 01110011 00100000 01100010 01100101 00100000 01101111 01101110 00100001

This translates to: "May the odes be good, and the ones be on!"

I hope that the ideas for new HTTP methods will inspire developers to create innovative solutions that benefit society and promote well-being. Thank you!
