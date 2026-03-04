# Fall 2025

…

Docs for OpenAI’s `/v1/completions` API: [https://platform.openai.com/docs/api-reference/completions](https://platform.openai.com/docs/api-reference/completions)

Independent study:

- [https://grad.engineering.ucsc.edu/independentstudy/](https://grad.engineering.ucsc.edu/independentstudy/)

- Objectives: (what we want to learn/show)  
  - Demonstrate the idea of Zeroconf AI by making a locally discoverable server that implements the OpenAI API while announcing its presence on the local network. One or two example apps will be created that can discover this service and route requests through it.  
- Expectations (how Joey will do it)  
  - Student will maintain notes in google drive, code on a public github, and be ready to show demos in weekly meetings. A written report, demonstration video, and accompanying source code repository will document the work by the end of the quarter.  
- Course number CMPM 297  
- Hours: 14 solo, 1 with advisor

## [RouteLLM](https://github.com/lm-sys/RouteLLM) is a framework for serving and evaluating LLM routers \- save LLM costs without compromising quality   [mDNS options](https://github.com/homebridge/homebridge/wiki/mDNS-Options)  [FastAPI Docs](https://fastapi.tiangolo.com/#example-upgrade)  ⭐[OpenRouter](https://openrouter.ai/) 

# Oct 9, 2025

[OpenAI connected apps](https://openai.com/index/introducing-apps-in-chatgpt/)  
This reminds me of when I told you “ai will be the phone.” I think that OpenAI is trying to make an all around platform where users just type something in, and then AI opens another app and hits the button to do something for them.

Although I will say, I am slightly bearish when it comes to this now. I think as a user I would just rather use the ui of an app. 

ChatGPT has also kind of tried this before with Custom GPTs, which are basically out the door at this point. This makes me realize how important this project is. Instead of connecting Apps to to the models like OpenAI thinks the future is, we are bringing AI to the apps instead. I realize that last sentence sounds AI generated and I haven’t fleshed this idea out yet, but it is something motivating me.

[https://x.com/karpathy/status/1977755427569111362](https://x.com/karpathy/status/1977755427569111362) 

Oct 15, 2025  
Link to Joey’s project on GitHub: [https://github.com/jperrello/Zeroconf-AI](https://github.com/jperrello/Zeroconf-AI)

Assume that there are multiple devices in one home. 

Missing one worked out use case

General confusion and question for Adam:

In our last meeting, you wanted me to think about scenarios where we have more than one provider, more than one service, and what if either/both go down. This made me think about creating a singleton. One service discovery process that runs once, maintains a registry of available services, and updates as services come and go on the network. 

What does this service need to do?  
The three things Adam had talked about:

- Add new services when the are discovered with mDNS  
- Remove the services when they go offline  
- Update the services \*implement  
- Allow the client to pick which services they want to use

# 10/21:

issues:

* When client is running and a service is added, the displayed list doesn't immediately update ![][image1]  
* When a service is disconnected in the middle of client prompting an agent, they receive the error messages but they arent returned to the menu. They need to enter a prompt and then they’ll get an error message and return to menu ![][image2]  
* When a service is disconnected and client is in the selection menu, they receive the error messages but the menus arent updated. The user needs to enter a number for the menus to reset ![][image3]  
* Sometimes on first boot of client only one instance is found. I think this is because Zerconf is slightly delayed

# Oct 22, 2025

### Notes prior to meeting:

Problems i can see with my current code:  
server.py: 

* the name of the service is currently hardcoded, I did not have time nor did I figure out how to name each service being registered different.  
* Find\_port\_number only searches from port 8080- 8100  
* Line 140, we shouldn’t automatically find a new port number but instead let the person setting it up choose one or at least have the option to have the computer find one rather than just doing it

client.py:

* The enum updated is not being used yet because i havent implemented updated services yet  
* This means update\_service in ZeroconfAIListener is a no-op right now and just adds services to the network  
* chat() currently hardcodes an llm model into the parameters. This is because i didnt have time to configure the model. I think this will eventually be server-side.  
  * Same goes for max\_history  
* Verify\_service\_health has a hardcoded timeout  
* All the problems I listed on the previous page, this is probably issues with my demo

What I think my next steps should be:

* Add updated service functionality  
* Allow person setting up the server to choose the max\_tokens and models being used  
* Add other API options (not just OpenRouter)  
* Thread safety?  
* Retry logic or automatic failover to another available service if a service goes down while chatting

### During Meeting

We are trying to emphasize the protocol:

- Lookup MDNS: `_zeroconfai._tcp._local`  
  - This should return a collection of IP address and TCP port pairs (with priority)  
- For each one, treat it has an http endpoint to request:  
  - `http://$IP:$PORT/health`  
- If a server seems healthy, request things you would expect from an OpenAI-compatible server:  
  - [http://$IP:$PORT/v1/models](http://$IP:$PORT/v1/models)  
  - [http://$IP:$PORT/v1/chat/completions](http://$IP:$PORT/v1/chat/completions)  
- To monitor if service is still healthy, periodically check the `/health` endpoint.  
- To monitor for more servers, periodically to the MDNS lookup again.

If someone wants to use ZeroConf AI in a new language, they need:

- A library for MDNS  
- A library for HTTP (or one that speaks the OpenAI completions protocol, which is just a specialized use of HTTP)

Let’s have multiple servers, each specialized to one use case:

- gemini\_proxy\_server.py  
  - provides access to anything you can get with a Gemini API key  
- ollama\_proxy\_server.py  
  - Provides access to any of the models served by ollama on the local machine  
- fallback\_server.py  
  - It responds to health checks but it declares that it has no models available.  
  - it provides one model called “dont\_pick\_me” that always responds “I told you so.”

Let’s have multiple clients, each specialized to one use case:

- simple\_chat\_client.py  
  - Automatically discovers and selects the first model from the first provider and lets you have a dead-simple text chat.  
  - This should be optimized to have the fewest distracting lines of code. Cut features to make it simple.  
- Local\_proxy\_client.py → for AI apps that don't know zeroconfai  
  - This one runs an OpenAI compatible server endpoint locally that will route request to other servers discovered via ZeroConf.  
  - Perhaps make this one be more industrial grade.  
  - Ideally, you could point a local app like 5ire ([https://github.com/nanbingxyz/5ire](https://github.com/nanbingxyz/5ire)) or Jan ([https://www.jan.ai/](https://www.jan.ai/))  
- Playlist\_generator\_client.py →  for apps that aren't aren't chat focused  
  - This is a mock application that has a list of plausible music tracks and it will try to find an appropriate local AI service if available but still be able to run even if one can’t be found.

At least one non python example

#  10/28

In all three new servers (gemini, ollama, and fallback) everything past the “Setting up the service” comment is the same. I was going to move this all into one file but I wasn’t sure since adam wanted these to all be their own standalone examples.

* Problem with this: the service\_name variable in register\_zeroconfai gives the name of the service hardcoded ie. for gemini server it is: service\_name \= f"Gemini.{service\_type}"

In [client.py](http://client.py) I made a model discovery method called get\_available\_models which just sends a request to f"{url}/v1/models" and returns a list of names and ids from an endpoint.  
chat() uses get\_available\_files but  just defaults to the first model in the list.  
Finished all three server files (gemini, ollama, and fallback). One question about gemini server:

* “provides access to anything you can get with a Gemini API key” I dont know what this means so i just picked four gemini models that cover all of its abilities (image generation, etc)

What I accomplished today:  
I made the three server files that Adam told me to make: gemini, ollama, and fallback. All three function similar and I feel like i could rewrite or refactor this code just so I am not copy pasting so much ( i brought up more detailed explanations in previous notes from today). The gemini server was the easiest because I was just able to copy most of what I had from my previous server file (still on github but probably is outdated now). Ollama server reuses a lot of the same code as well, just had to tweak some stuff with sending payloads and requests because ollama works differently than making api requests to OpenRouter. Fallback server was the easiest to implement. Again, much of it was just copy pasted work from before with minor tweaks. Biggest difference now is that the model is set to dont\_pick\_me and no matter the client request it just responds with a  random AI generated quip about picking the dont pick me model.

[client.py](http://client.py) needed some changes which i kinda got wrapped up in even though i will be making multiple clients. I just wanted to keep using [client.py](http://client.py) in order to test my three different servers. I also figured that it will in the long run help me with the future clients. Now the client actually discovers multiple servers all with multiple models. Right now they default to the first model in the list of models at the /v1/models endpoint, but this can be configured differently. Additionally, I was having some issues with how ollama timing out so i got rid of the persistent health checking that is just always serving a bg thread. My chat() method already marked services as unavailable if the user entered a message to them so i decided to just use that. This means that now a user has to actually type a request to see if the server is down but honestly this would only happen in extreme cases like services that crash/disconnect won't be automatically removed from the list until someone tries to use them. Get\_available\_models is important to read and understand because it tells you that the models in the server files needed to be me consistent with ollamas naming pattern models \= \[{"id": name, "object": "model", "owned\_by": "google"}

Lastly, I made the simple\_chat.py file which is the most barebones way of just quickly connecting to the first possible chat client. It is meant to be the least distracting implementation of zeroconfai.

Oct 29, 2025  
10/29 Meeting notes:

Started work on priorities for servers.

Todo:

- Install 5ire or Jan, get it to use ollama directly to start  
- Update local\_proxy\_client to aggregate available models across all local services

# Nov 5, 2025

Meeting Notes:

[https://github.com/janhq/jan/issues](https://github.com/janhq/jan/issues) 

[https://openrouter.ai/docs/api-reference/models/get-models](https://openrouter.ai/docs/api-reference/models/get-models)

[https://github.com/janhq/jan/issues/6893](https://github.com/janhq/jan/issues/6893) 

# Nov 19, 2025

Adam’s notes on Joey’s demos:

- It has a name: Saturn\!  
- There’s a plugin for VLC that has a “Chat with Saturn” menu option  
  - When selecting it, it launches the bridge Python script (and kills the script when VLC closes)  
- The VLC demo application should somehow demonstrate something that is only possible by combining VLC data with AI – maybe a “roast my personality” based on my currently open files. We want it to legitimize niche features in non-AI apps.

Idea:

- Pitch fellow CSE MS students on having a MS project where they integrate Saturn into another app.  
- 

Possible integrations:

- IDEs  
  - Cline / Roo  
  - Cursor / Windsurf  
  - GitHub Copilot  
- Open WebUI  
- Note-taking apps  
  - Obsidian  
  - Logseq  
  - Joplin  
- Home Assistant  
- Desktop AI chat apps  
  - [Jan.ai](http://Jan.ai)  
  - LM Studio  
  - GPT4ALL  
  - AnythingLLM  
- Workflow automation systems  
  - N8n  
- Content creation  
  - OBS  
  - Blender  
  - (any content creation tool with a plugin system)  
    - ~~Photoshop~~  
    - Krita \- [https://docs.krita.org/en/user\_manual/python\_scripting/install\_custom\_python\_plugin.html](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html)

11/26  pre meeting:  
New DNS flow:  
![][image4]  
OWUI works:  
![][image5]

Also roast extension has been created, and the html page has been successfully updated

Goals for this week:

Talk to Mozilla people: [https://discourse.mozilla.org/tag/participation](https://discourse.mozilla.org/tag/participation)   
[https://www.mozilla.org/en-US/about/forums/](https://www.mozilla.org/en-US/about/forums/)  
[https://www.mozilla.org/en-US/contact/](https://www.mozilla.org/en-US/contact/) 

Post on: [https://www.reddit.com/r/LocalLLM/](https://www.reddit.com/r/LocalLLM/) 

Reach out to Clad Labs:  
[https://www.cladlabs.ai/blog/introducing-clad-labs](https://www.cladlabs.ai/blog/introducing-clad-labs) key takeaway: autonomous coding agents by Q2 2026  
CEO’s Twitter:  
[https://x.com/zzzbuggg](https://x.com/zzzbuggg)   
Other Employee:  
[https://x.com/xkevin\_le](https://x.com/xkevin_le)  
Company Itself:  
[https://x.com/cladlabs](https://x.com/cladlabs) 

Ollama Integration based on our old issue:  
[https://github.com/ollama/ollama/issues/10283\#issuecomment-3561448581](https://github.com/ollama/ollama/issues/10283#issuecomment-3561448581) 

I had Opus 4.5 look up other companies and applications to integrate with here:  
[https://github.com/jperrello/Saturn/blob/main/research/saturn-integration-opportunities.md](https://github.com/jperrello/Saturn/blob/main/research/saturn-integration-opportunities.md)   
\-zed

I am also interested in eduroam, but couldn’t find a legitimate contact:  
[https://eduroam.org/](https://eduroam.org/)   
Perhaps Eduroam is too big to do something like this..   
My original plan of setting up at baskin may be the best idea. 

Currently working on implementing this with my other class project [MiniStS](https://github.com/iambb5445/MiniSTS), since they use api calls to openAI

Nov 26, 2025 1:00 PM Meeting Start  
Zeroconf library for openwebui function  
Demo video of the VLC roast extension  
Zed, neovim extension  
[https://incommon.org/solutions/](https://incommon.org/solutions/)   
Single pdf project report on why the world needs this, here is how it works.  
	\-bring up existing work  
	\-background  
	\-no code  
Meeting starts at 1:30 next week, not 1  
Made follow up post on r/RASPBERRY\_PI\_PROJECTS: [https://www.reddit.com/r/RASPBERRY\_PI\_PROJECTS/comments/1pcor8i/running\_local\_llm\_servers\_has\_never\_been\_easier/?utm\_source=share\&utm\_medium=web3x\&utm\_name=web3xcss\&utm\_term=1\&utm\_content=share\_button](https://www.reddit.com/r/RASPBERRY_PI_PROJECTS/comments/1pcor8i/running_local_llm_servers_has_never_been_easier/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) 

Made a post on r/OpenWebUI: [https://www.reddit.com/r/OpenWebUI/comments/1pcqric/run\_any\_model\_provider\_on\_openwebui\_immediately/?utm\_source=share\&utm\_medium=web3x\&utm\_name=web3xcss\&utm\_term=1\&utm\_content=share\_button](https://www.reddit.com/r/OpenWebUI/comments/1pcqric/run_any_model_provider_on_openwebui_immediately/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) 

This one got interesting replies telling me to look up: [LiteLLM](https://www.litellm.ai/) and [Requesty](https://www.requesty.ai/landing3?utm_source=google&utm_medium=cpc&utm_campaign=openrouter_search&utm_term=requesty%20router&gad_source=1&gad_campaignid=22680385099&gclid=CjwKCAiA3L_JBhAlEiwAlcWO5zJY3azCOuDujSUP3X0MGexVwmO9I6AFPbhil6DFicRBDP8bltDphRoCAiEQAvD_BwE)

* Both of these applications focus on routing requests, which tells me I was not clear enough in my original post

## OWUI function now uses the zeroconf library.

# Dec 3, 2025

Remove failover claim from openwebui function’s valves  
[https://github.com/open-webui/open-webui/discussions/19310](https://github.com/open-webui/open-webui/discussions/19310)   
[https://grad.engineering.ucsc.edu/advising/planning-to-graduate/\#filing](https://grad.engineering.ucsc.edu/advising/planning-to-graduate/#filing) 

People to be the first member of the reading committee:

- Interested in networking  
- Interested in GenAI

[https://catalog.ucsc.edu/current/general-catalog/academic-units/baskin-engineering/computer-science-and-engineering/computer-science-and-engineering-ms/](https://catalog.ucsc.edu/current/general-catalog/academic-units/baskin-engineering/computer-science-and-engineering/computer-science-and-engineering-ms/) 

[https://grad.engineering.ucsc.edu/independentstudy/](https://grad.engineering.ucsc.edu/independentstudy/) 

12/11

Ram is on board with the project \- going to meet at start of next quarter   
Need to write a report for Saturn and a title page  
	Already made title page  
	There are no requirements for paper \- it is at the discretion of the reading committee  
What are the next steps?

Dec 12, 2025Meeting

Worked on fixing final report pdf.  
	Added footnotes. Stopped being so vague  
Got rid of my own personal opinion, anchored in other people’s opinions.

Saturn “beacons” \- have a server client and “beacon” these beacons periodically announce and provide api keys for a limited time for people to use while on the network, but when they leave there are no more keys.

Look at over the break:

- Make a Saturn Beacon: A script that merely locally announces how to access some other service beyond the LAN.  
  - DeepInfra has a way of generating short-lived API keys: [https://deepinfra.com/docs/advanced/scoped\_jwt](https://deepinfra.com/docs/advanced/scoped_jwt)  
    - This lets you give someone a key that will expire soon.  
    - Make a service that, via mDNS, gives out a key that only lasts a few minutes and keeps the key updated.  
    - Modify one or more of your clients to notice if the Saturn announcement includes an API key and uses that as part of the next request.  
    - Watch out that in one place of the documentation there is a typo: “api\_key\_name” should bd “api\_token\_name” or something. If you use the wrong string, you’ll see an error message in the HTTP response indicating the correct name.  
    - Adam suggest not bothering with a spending limit, only using expires\_delta  
    - Watch out that mDNS strings probably can’t be longer than 250 characters without truncation  
  - Skip the models, default to all models if none specified

12/15  
A beacon is more formally called “ephemeral credential distribution.” 

Jan 6, 2026  
What CC said when asked what layer of OSI we are working on:  
\> what layer of the osi model do you think i am working on? ultrathink

● This is a fascinating question for your thesis framing. Let me think through this carefully.

  The simple answer: Layer 7 (Application)

  All the protocols Saturn uses are Application layer:  
  \- mDNS/DNS-SD → Application (runs over UDP)  
  \- HTTP/REST → Application  
  \- JSON/SSE → Application data formats

  But that's not the interesting answer.

  Saturn's purpose maps more closely to Layer 5 (Session Layer):

  | OSI Layer 5 Concept   | Saturn Implementation                                      |  
  |-----------------------|------------------------------------------------------------|  
  | Session establishment | Service discovery \- finding where to connect               |  
  | Dialog control        | Priority-based routing \- which service handles the request |  
  | Token management      | Ephemeral JWT distribution \- credentials to start sessions |  
  | Synchronization       | Key rotation \- keeping credentials valid across time       |

  The beacon makes this clearer:

  The beacon doesn't carry user data. It doesn't process requests. It distributes credentials needed to establish sessions elsewhere. This is textbook Session layer behavior \- it's coordinating how sessions get started, not the sessions themselves.

  Traditional L5 example (Kerberos):  
    Client → KDC: "I want to talk to Server X"  
    KDC → Client: "Here's a ticket (time-limited credential)"  
    Client → Server X: Uses ticket to authenticate

  Saturn beacon:  
    Beacon → mDNS: "Here's a JWT (time-limited credential) for DeepInfra"  
    Client discovers → extracts ephemeral\_key  
    Client → DeepInfra: Uses key to authenticate

  My thesis-worthy framing:

  Saturn operates at Layer 7 technically but provides Layer 5 functionality semantically. It's middleware that:

  1\. Abstracts L3 (IP addresses) \- clients don't need to know IPs  
  2\. Abstracts L4 (ports) \- auto-discovery finds ports  
  3\. Implements L5 (session coordination) \- service selection, credential distribution  
  4\. Uses L7 (mDNS, HTTP) \- as transport for the above

  Or provocatively: Saturn is "Layer 5.5" \- it sits between session establishment and application protocols, using L7 protocols to solve L5 problems.

  For your masters presentation, I'd frame it as: "Saturn provides Session-layer service discovery using Application-layer protocols, enabling zero-configuration access to AI services."

# 

# Winter 2026

# Jan 6, 2026

- Joey’s courses:  
  - CMPM 280G \- 2u  
  - CMPM 297 (Independent study) 5u  
  - CSE 247b \- 5u  
  - CSE 240 (AI) \- 5u  
- MS Thesis vs MS Report  
  - J needs to turn in a report to the reading committee (Adam \+ Ram?)  
  - Title page with signatures  
- Independent study  
  - Objective  
    - Prepare MS thesis draft on the Saturn AI service discovery protocol. Develop app integrations to show the breadth and depth of impact possible for the protocol. Run on-campus connectivity experiments to understand the in-situ usability of the protocol.  
  - Expectations  
    - Maintain research notes in Google Drive and software project details in a public GitHub Repository  
    - Build research prototypes and conduct relevant experiments.  
- Other projects:  
  - **Clients** (things that try to find servers)  
  - **Servers** (things that announce an endpoint they offer for themselves)  
    - Figure out how to run a rely on an embedded device  
      - Raspberry Pi 5  
      - A low-ish end wifi router   
        - Adam has an Ubiquiti EdgeRouter X ER-X  
        - Ask Ram what’s a good representative example  
        - [https://www.gl-inet.com/](https://www.gl-inet.com/)  
    - Make a simple web-based admin interface for controlling the proxy  
      - Set name, priority, back-ends, API keys, hours of access, prompt injection, rate limits, beacon mode.  
  - **Beacons** (things that announce temporarily access to third-party service)  
    - True beacons only speak mDNS, no HTTP(s).

Fill out independent study form and send it to Adam  
![][image6]

Taken from: [https://registrar.ucsc.edu/calendars-resources/academic-calendar/](https://registrar.ucsc.edu/calendars-resources/academic-calendar/)   
![][image7]  
Taken from [https://docs.google.com/document/u/1/d/e/2PACX-1vTRRQ4MYbDzxqDAWOdLYM0BIYUz33WCk\_5ePVc3\_cdMDdyvq2Ef2fi1m4TyHyxTOV6mPJ6lk-AO4iXQ/pub\#h.ny3hvokyzq9h](https://docs.google.com/document/u/1/d/e/2PACX-1vTRRQ4MYbDzxqDAWOdLYM0BIYUz33WCk_5ePVc3_cdMDdyvq2Ef2fi1m4TyHyxTOV6mPJ6lk-AO4iXQ/pub#h.ny3hvokyzq9h) 

Jan 13, 2026 Pre meeting  
router has a tiny 580MHz MIPS processor. Compiling Go code directly on it would take forever (if it even worked). So we cross-compile on the fast laptop, then just copy the finished binary over.  
![][image8]  
![][image9]  
![][image10]  
![][image11]  
Clients using dns-sd could not find the beacon.   
Zeroconf library clients could, but wouldn’t actually start.

This fix was simple, just passed in the hostname to client rather than running inet\_ntoa  
Successful Test:![][image12]  
This client does use dns-sd, need to keep working to figure out why zeroconf is not working.  
Key properly rotates on router:  
![][image13]  
Memory Stats while beacon is running:  
![][image14]

# Jan 13, 2026 Meeting

ANS:  
[https://aboutus.godaddy.net/newsroom/news-releases/press-release-details/2025/GoDaddy-advances-trusted-AI-agent-identity-with-ANS-API-and-Standards-site/default.aspx](https://aboutus.godaddy.net/newsroom/news-releases/press-release-details/2025/GoDaddy-advances-trusted-AI-agent-identity-with-ANS-API-and-Standards-site/default.aspx)   
[https://www.agentnameregistry.org/](https://www.agentnameregistry.org/)   
A2A:  
[https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)   
UCSC eduroam iot devices:  
[https://its.ucsc.edu/services/network-and-infrastructure/network-and-connectivity-management/ucsc-devices-wireless-service/](https://its.ucsc.edu/services/network-and-infrastructure/network-and-connectivity-management/ucsc-devices-wireless-service/)   
E2-256 

To do soon:

- Run an on-campus mdns reachabiltiy experiment  
- Learn about openwrt packages  
  - How do you publish one?  
  - How does one provide a UI component?  
    - Luci   
  - A2A (two CC talking to each other) is put on back burner. Finish Saturn first

- Make an openrouter beacon that does automatic key rotation?  
  - Doesn’t need to be in Go, but it could be  
  - 

# Jan 20, 2026 

We found that eduroam and UCSC-guest seem to implement some kind of either **AP Isolation** and or multicast traffic blocking. On either network, we could ping and run an http service, but we couldn’t resolve locally announced names or services. So, it seems like non-IT people would not be able to provision Saturn services in this kind of network setting, but maybe the IT people could do it.

We found that the Mango router offers services on the LAN side network but not the WAN side network, at least with the current Go code. This makes sense.

The openrouter beacon worked properly. When Adam was on the Mango’s network, he was able to browse for saturn services, find an temporary API key, and then use it to make an LLM request that the Mango would have no hope of decoding (https directly to openrouter).

When we looked at the Luci settings page for the plugin, it was confusing that “openrouter” referred to both a local proxy server (that could handle LLM requests) and also a way of giving out temporary keys. These roles should be disambiguated.  
![][image15]  
![][image16]![][image17]  
Jan 25, 2026  
Running into problem with starting my saturn services on the router.   
Hard-Float vs Soft-Float ABI Mismatch  
Mango (GL-MT300N-V2) router uses soft-float MIPS (indicated by the sf in the linker path):  
  /lib/ld-musl-mipsel-sf.so.1 \-\> libc.so

  But the toolchain being used (mipsel-linux-musl-cross.tgz) produces hard-float binaries that expect:  
  /lib/ld-musl-mipsel.so.1  (doesn't exist, and symlink won't help)

  The \-ash: not found error is misleading. It doesn't mean the file is missing—it means the dynamic linker specified  inside the ELF binary cannot be resolved, or the ABI is incompatible.

 Why the Symlink Doesn't Work

  Hard-float and soft-float are incompatible ABIs:  
  \- Hard-float: Uses hardware FPU instructions and floating-point registers  
  \- Soft-float: Emulates floating-point in software

  Creating a symlink from the hard-float linker to the soft-float libc won't work because:  
  1\. The binary contains hard-float instructions the soft-float libc can't execute  
  2\. The calling conventions are different (arguments passed in different registers)

  Here's the important finding from that https://kauruus.github.io/posts/2023/10/09-cross-compile-rust-program-for-mipsel/ and  
  the https://github.com/rust-lang/rust/issues/34922:

  Rust's mipsel-unknown-linux-musl target is ALREADY soft-float\!

  The Rust target specification already includes "+mips32r2,+soft-float". The problem isn't Rust generating wrong code—it's that we're using a hard-float C linker to link soft-float Rust code.  
![][image18]  
 We only need to change the C toolchain in the Dockerfile. The changes are:  
![][image19]  
 Are We Relying on External Code?  
Mostly no.   
![][image20]  
The entire build is self-contained. You download a tarball, everything compiles from source (including Rust's standard library via build-std), and the result is a statically-linked binary.  
  The only external dependency is musl.cc hosting the toolchain tarball, which has been stable since 2021\.  
Changes:  
  1\. saturn-router/cross/Dockerfile.mipsel  
  \- Changed toolchain from mipsel-linux-musl-cross.tgz to mipsel-linux-muslsf-cross.tgz  
  \- Updated all env vars from mipsel-linux-musl-\* to mipsel-linux-muslsf-\*  
  \- Added comments explaining the soft-float requirement

  2\. saturn-router/Cross.toml  
  \- Updated comments to document the soft-float toolchain choice

 \=== Build Results \===  
  target/mipsel-unknown-linux-musl/release/saturn: ELF 32-bit LSB pie executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically  
  linked, interpreter /lib/ld-musl-mipsel-sf.so.1, stripped  
  Raw binary size: 2.3M

interpreter /lib/[ld-musl-mipsel-sf.so](http://ld-musl-mipsel-sf.so).1 confirms the fix, it is exactly what the router has.

# Jan 27, 2026

Joey did not accomplish as much work as he wanted to, but he is completely done with coding the LuCI ui and saturn beacon on the router.  The confusion about beacon vs HTTP has been solved. All things running on router need at least some HTTP in order to ping the health endpoint, but to differentiate a beacon with a server, there is an ephemeral key option that when clicked asks for key generation endpoint and instead only distributes keys instead of proxying requests.

Can show evidence but it would require starting the router which means internet issues.  I would like to show off on friday with the other independent study students.

As for research, this is where joey fell short of the work he wanted to get done. I learned a little more about AP isolation and some Bonjour gateway things. 

“I am Joey, I made [https://jperrello.github.io/Saturn/](https://jperrello.github.io/Saturn/) as part of my computer science & engineering MS program at UC Santa Cruz. I’m interested in using Claude Code heavily in my thesis writing process. Begin by interviewing me to draw the key ideas and context out of me, using web search tools and keeping local notes in markdown where appropriate. We’ll use this folder across several Claude Code sessions to eventually get the thesis written in latex and compiled down to a satisfactory pdf that my advisor(s) can review. I’m not ready to write the whole thing, just get the project started today. Please act as a wise robo-advisor for me today.”

Research contribution (now what it does, but what it shows/proves/enables):

- GenAI access ought to be like printer access, if you get on the wifi, you get the AI too.

Jan 31, 2026  
Get multiple Saturn providers running on Open Code. The models list doesn't update when new providers are joined on the network when open code is already running. When multiple servers are running and open code is started afterwards only one provider is shown . Have not tested files being modified or any usual coding agent things using Saturn yet .  There is a weird bug where when you send a message and you receive a response and see it in the agent, open code itself seems to be waiting for that response to return when it already has so you can't send any messages past the first one because they are just thrown in queue .   
Feb 1, 2026  
After Ralphing, beading, and testing struggling to get opencode to: 

1. Refresh models/providers list when saturn taken offline/online  
2. Have opencode actively trigger \[DONE\] when saturn returns an ai response

So I gave it this prompt:   
“””  
 all day i have been trying to fix bead issue Saturn-1wg. you can see by the screenshots, as well as the issue itself, and the previous attempt with  
    @claude\_prompt.md . I wonder if you think this problem is inheret with C:\\Users\\jperr\\Documents\\GitHub\\Saturn\\ai-sdk-provider-saturn\\upstream ? I will explain the  
  purpose of what I am doing with you know. Saturn is my master's project \-- and my advisor Adam and I want a practical way of using Saturn in the wild. We originally had  
  the idea of creating a Saturn plugin for OpenCode, but my advisor summed it up best by saying: "However, there are many other apps out there like OpenCode now, so we  
  should try to be more strategic than just making a plugin for each one. I think there's a way." When I look into the source for OpenCode, I spotted a list of  
  "BUNDLED\_PROVIDERS" representing all of the LLM providers that OpenCode knows about by default (without the need to install additional plugins). One thing that jumped out  
  at me was that almost every single one of the bundled providers was implemented using an npm package associated with the AI SDK organization. Take a look:  
https://github.com/anomalyco/opencode/blob/8c05eb22b1a78843f982b896464feae19d2c9dc1/packages/opencode/src/provider/provider.ts\#L56  
  AI SDK is this upstream project that is trying to make it easy to support many different LLM providers. If we could get Saturn support here, getting Saturn support in most  
   downstream applications would only required a few lines of code change. For example, a camera app developer might decide to build on AI SDK. Here are the top-level docs  
  for using providers and models in AI SDK: https://ai-sdk.dev/docs/foundations/providers-and-models  And here are the top-level docs for creating custom providers and  
  getting them published: https://ai-sdk.dev/providers/community-providers/custom-providers  
  Therefore, I wanted to create the sdk and use it in opencode. Turns out Saturn is very complex for a number of different reasons, but it has been a major headache. I am  
  starting to think of how I should even go about fixing this bead issue. It seems so integral to how opencode functions to fix this problem. But I really struggle to find a  
   way to bridge this gap. my professor said: " getting Saturn support in most downstream applications would only required a few lines of code change" and that is sticking  
  with me. This has not been a few lines of code fix for opencode. but maybe it needs to be. perhaps saturn should have an mcp where someone can just ask about their saturn  
  services and that triggers discovery. I am kinda at a loss. Take all of this in, but dont propose a fix or coding. Instead use tthe AskUserQuestion tool. I will provide no  
   guidance on what these questions should be. They can literally be about anything. Just genuine questions that arise from digesting all this context  
“””  
Here were its questions with my answers:  
![][image21]![][image22]![][image23]![][image24]  
![][image25]![][image26]![][image27]![][image28]  
![][image29]  
![][image30]  
![][image31]  
![][image32]  
Feb 2, 2026  
Using the saturn python package:

  Yes, it's inherently risky. Storing secrets in plaintext files is never "secure" \- it's just "acceptable risk" for CLI tools.

  The risks:  
  \- Anyone/anything with access to your machine can read \~/.saturn/.env  
  \- Malware, other users on shared machines, backups to cloud storage  
  \- If your laptop is stolen, those keys are exposed

  Why it's the industry standard anyway:  
  \- The alternative is worse UX → users put keys in shell history, scripts, or git  
  \- At least \~/.ssh/ and \~/.aws/ are in known locations that security tools can monitor/audit  
  \- File permissions can restrict access (on Unix: chmod 600\)

  What's actually more secure (but we didn't implement):  
  \- OS keychain integration \- Windows Credential Manager, macOS Keychain  
  \- Encrypted at rest \- require a password to decrypt keys  
  \- Short-lived tokens only \- never store long-lived keys

  For Saturn specifically, the beacon mode is actually more secure than storing keys \- it generates short-lived ephemeral keys that expire. The irony is we still need  
   the provisioning key to create those ephemeral keys.

  Summary of the fix:  
  \- Added load\_dotenv(\~/.saturn/.env) to the runner  
  \- API keys stored alongside configs in \~/.saturn/  
  \- No git leakage risk since it's outside any repository

  The \~/.saturn/ structure is now:  
  \~/.saturn/  
  ├── .env          ← API keys (OPENROUTER\_API\_KEY, etc.)  
  ├── services/     ← service configs (\*.toml)  
  └── run/          ← runtime PID files

# Feb 10, 2026

Rename: Background and Related Work \-\> Background

What service discovery exists and why didnt we use them  
[https://en.wikipedia.org/wiki/Zero-configuration\_networking](https://en.wikipedia.org/wiki/Zero-configuration_networking)   
NetBIOS – emphasis on Windows  
WS-Discovery \- seems modern, but maybe windows emphasis   
Universal Plug and Play- adam says complicated, somewhat old  
DLNA  (maybe propriety)

In coverage of mDNS we should mention avahi and Bonjour   
	What is a txt record and what is in them?  
	

Also Background:   
Where text completions are being used?   
There are hosted chat apps like librechat and openwebui  
There are coding agents that allow you to configure your own endpoints   
Some coding tools like VS code, have mDNS for discovering debugging targets

Voice typing/ transcription cleanup:  
Most have an on device voice model and then use off device model to make sound profession/fix grammar

DHCP – explain how dhcp operates differently on the network stack than saturn. 

Explain why we chose Saturn over these methods 

Most content in background section is about mDNS but you have less space for each of these above things 

Audience for Saturn  
	LLM inference provider  
		Wants people to use services   
	IT person  
		Wants to offer services to house guest  
	End user  
		Wants magic sparkle button to work  
	App developer  
		Wants to offer magic sparkle button 

```
Design
  Goals
  Audiences
  Concepts
    - Endpoints (OpenAI compatible endpoint: might be local inference or a proxy to a remote service)
    - Beacons (mDNS response announcing an endpint)
    - Priorities
    - Ephemeral Keys

  Protocol Specs
    - Official name: _saturn._tcp._local
    - Example TXT record details
    - Expecations on the advertised endpoints:
      - /health
      - /v1/model/list
      - /v1/chat/completions
  Architecture Decisions

```

Security section: 

* Find threat models for security claims  
  * Two threat models: I dont want big corporations like anthropic getting my data and I do not trust the system administrator of my office or house.


  
Feb 16, 2026  
**Goal:** Build a writing skill for Claude Code so that when I ask it to draft/revise sections of thesis, it follows a consistent quality bar.   
It is separated into two parts:  
The general principles act as a universal checklist, and the reference files give section-specific guidance.

Prompt for academic-writing skill. 

```
Create a skill called academic-writing. Here's the spec:
YAML frontmatter:
name: academic-writing
description: "Use this skill whenever Claude is writing prose, essays, academic content, reports, or any long-form written output, even if the user doesn't explicitly mention writing quality. Trigger for any drafting, revising, or editing of written sections — including when the user pastes text and asks for feedback."
SKILL.md body:
Leave a clearly marked placeholder section at the top for general writing principles (I'll fill this in myself)
Below that, define the core workflow. Claude must follow this loop for ALL writing output: (1) draft freely, (2) evaluate the draft against the general checklist AND the section-specific guidelines, (3) revise based on the evaluation, (4) present only the revised version. Do NOT skip straight to a polished draft — the evaluate-and-revise step must actually happen.
At the bottom, add section routing. Before writing, Claude identifies which section it's working on and reads the corresponding reference file. The sections are: abstract, introduction, background, design, implementation, evaluation, discussion, conclusion. Apply both the general principles and the section-specific guidelines.
Reference files: Create references/ with empty placeholder files for each section: abstract.md, introduction.md, background.md, design.md, implementation.md, evaluation.md, discussion.md, conclusion.md. Each file should just have a header and a one-line placeholder like "Section-specific guidelines go here."
Don't fill in any of the actual writing guidelines — I'll do that myself. Just give me the structure and the workflow logic.
```

Writing the general-purpose writing principles (didnt fill in myself):  
[https://thegraduatewritingguy.com/thesis/](https://thegraduatewritingguy.com/thesis/) 

First prompt sent to CC: 

```
Read @writing-notes.md and the existing .claude\skills\academic-writing\SKILL.md. Your job is to fill in the [TO BE FILLED IN BY USER] placeholder in the General Writing Principles section.
Rules:
Each principle must be a concrete, evaluable rule — something you could check against a paragraph and say "pass" or "fail." No vague aspirations like "write clearly."
Include a short example (good vs bad) only when the rule is ambiguous without one. Most rules won't need examples.
The full SKILL.md must stay under 200 lines total. The General Writing Principles section gets roughly 120 lines max. Be ruthless about compression.
The notes file is input only. The finished SKILL.md must be fully self-contained — a different Claude instance reading only the SKILL.md (without the notes) must be able to apply every principle consistently.
Verification before you finish:
Re-read only the SKILL.md. For each principle, ask: "Could I evaluate a draft against this without any other context?" If no, the principle is too vague — rewrite it.
Count total lines. If over 200, cut.
Check for redundancy between principles. Merge any that overlap.
```

Writing abstracts  
[https://wilson.fas.harvard.edu/aphorisms/abstracts](https://wilson.fas.harvard.edu/aphorisms/abstracts) 

Design was taken from the filetree we drew out above on Feb 10

Background info was also partially taken from our notes above in feb 10\. But it also came from:  
[https://library.sacredheart.edu/c.php?g=29803\&p=185917](https://library.sacredheart.edu/c.php?g=29803&p=185917) 

The other sections were made with the help of claude

# Feb 17, 2026

Showed off skill, moons, and current draft.  
[https://arxiv.org/abs/2506.02153](https://arxiv.org/abs/2506.02153)   
Argumentation theory

Keystroke-Level model for evaluation on how easy saturn is to setup

**Post Meeting:**  
Was playing with the knowledge graph and realized that there werent actually THAT many edges – 217 to be exact. 

Decided to launch a team of agents to figure out if i am missing any edges from first pass.   
Why teams?

- Having one agent do it is too much context  
- Can have teams return their new edge proposals to me and the main claude  so we can check any hallucination or nonsense. 

```
i was playing around with the knowledge graph you
  made for moons and i noticed the low number of
  edges. i did digging and found out the papers had
  surprisingly low connections. I think we should
  launch a team to read through all the source
  material and tell us (me and you claude) its plans
  for new connections to draw from. that way we can
  verify that what they are making wont
  overcomplicate the project, and catch
  hallucinations. we will approve and then you can
  update moons accordingly
```

Afterwards I had 329 edges. 

This graph ended up being super helpful for me. I wanted to make more tools.

Feb 19, 2026  
Blind evaluation strategy:  
**Idea**: In order to prevent the claude agent that will be running the evaluation from gamifying the system we need to make it blind to what saturn is and blind to what the evaluation tests/metrics are. Claude mentioned a system called “Bloom that does this strategy but to detect agent sycophancy. Here is the blog post:   
[https://alignment.anthropic.com/2025/bloom-auto-evals/](https://alignment.anthropic.com/2025/bloom-auto-evals/)   
Github (has how to cite):  
[https://github.com/safety-research/bloom/](https://github.com/safety-research/bloom/)   
  1\. Traditional systems evaluation (evaluation-sketch.md): Latency benchmarks, interop matrices, cognitive walkthroughs, STRIDE threat models, exposure window math. These are established, defensible, appropriate for a systems thesis. They don't need Bloom.  
  2\. Bloom-inspired agent evaluation (plan.md): Blind agents in Docker, outcome grading, judge agents. This is creative and novel, but its validity depends  on whether "an AI agent can discover Saturn" maps meaningfully onto "zero-config is feasible for humans."

# Feb 24, 2026

Major todos:

- Read: [https://www.nngroup.com/articles/ten-usability-heuristics/](https://www.nngroup.com/articles/ten-usability-heuristics/)  
-   
- Try to have a live conversation with Ram about your thesis writing strategy.  
  - This mode of writing is fine with Adam as long as there is a clear and prominent 100%-human written explanation near the start (e.g. in the acknowledgement section) and some details on how the system works towards the end (e.g. in an appendix).  
  - Include: Why?  
    - Joey: Because I want to play with LLMs more.  
    - Adam: We want to be more systematic and comprehensive than the student would have been alone with only once-per-week guidance. Using this agent-assisted research flow, we:  
      - Detailed design fiction to reveal system requirements and use cases  
      - Created multiple interoperable technical prototypes  
      - Deployed an explainer website with human and agent-facing documentation  
      - …  
      - C2: Assisted in detailed cognitive walkthrough  
      - 

Claim 1:   
	Break down into requirements: what requirements would result in Saturn being feasible?  
Example: zeroconf is feasible on a network  
R1: you have to find the service on the network  
R2: I have scripts to do it just walk through a detailed explanation of saturn working on network  
R3: 

Claim 2:  
Need an initial “seed” of a human actually doing the walkthrough  
	I, Joey, need to do the walkthrough first to count the steps.   
	Then, we can have claude implement saturn in a script vs implement api key in a script and count the steps, tool calls, or research needed to complete it,

C1 is the most important super duper should be true, all the others are subclaims.

Claims and evidence alone are really good, it doesnt necessarily matter how weak they are initially.

```
I have this directory: /Users/jperr/Documents/cog_walkthrough I was hoping this
  could help us with the cognitive walkthrough of Claim 2. Each python file counts the number of
  steps inlined in hopes of comparison. here is the challenge: there are different levels of
  difficulty when it comes to Saturn. for this I wrote a short paragraph to explain:
  There is the person who configures Saturn on their private or institutional level, there is an
  app developer who wants to implement ai services into their system, and there is a common
  person who is on a network with Saturn and using an app with AI features. The person who is on
  the network and wants to use saturn is by far the person who has the least configuration
  burden. they just have to opt in to joining the wifi network. Typically they dont have to deal
  with any configuration, but I (joey) would argue this is not true because people typically have
  to pay to access AI features (need evidence) because AI featuress cost app devs money. This
  means the person has to enter a credit card and pay to use the app. This problem is what i
  tried to talk about in my motivation about accessibility to ai services, most people cant
  afford that or simply dont want to put in a credit card. <side note>App Devs typically have to
  configure stripe or something too if they put ai in their app because they need payments.</side
  note> .
  So these files are here to show the in house IT-person/system administrator and app developer
  who are setting up ai services. I am asking you, am i missing any steps here? What should I be considering that I am overlooking?
```

# Mar 3, 2026

Meeting Notes: 

Draft of acknowledgement for AI writing and appendix is written

* Tab is [here]()  
* 100% written by Joey  
* Not written in the first person. Uses “the author” instead of “I”  
  * Adam says to use I instead of the author and explain who the we is if uses we  
* The acknowledgement should include single links as evidence, the appendix has proper citations  
* Use active voice instead of passive when writing the thesis “I decided” instead of “it was decided” this allocates blame  
* Create an llms.txt file for the documentation website and talk about it in the appendix  
* 

Cognitive walkthrough for claim 2 has been completed for all three different audience members

* My evaluation results are in the cog\_walkthrough directory of the thesis and include multiple python walkthroughs of setting up a saturn service  
* I also have an interactive website visualizer  
* ..  
* ..

Claim one has three different requirements in order to prove that zero-config AI provisioning is feasible via mDNS/DNS-SD.

1. A Saturn service advertising on \_saturn.\_tcp.local. can be found by a  client with no prior configuration.  
   1. How should joey show this? Should I start a saturn server in one terminal and show dns-sd \-B output in another terminal? Should I use two different laptops on the same network? Should I use one of the integrations?  
   2. ..  
   3. .  
2. The information returned by discovery is enough to make a working AI API call.  
   1. This can be shown with a TXT record  
   2. ..  
3. Independent implementations in different languages/libraries all consume the same protocol.  
   1. We have so many different implementations already in the codebase  
   2. ..

Thesis currently has evaluation written as well as some other sections that have been refined through the ai detection ralph loop

* Ralph loop runs thesis.pdf through Sapling’s AI detection software and gets a score, if it has a high score the thesis is rewritten with the academic-writing skill to attempt to get a lower skill. Models typically fail at this multiple times so the ralph loop makes an agent constantly iterate to get a better score  
* Its okay if ai generated text sounds ai generated, it just needs to be a good use of the readers time.  
* ,,

Goal: Email Ram by Wednesday. What is needed before then? 

* One draft of the thesis  
  * Note that due to the nature of my thesis constantly being modified by agents, it may be slightly different on the github repo   
  * In order for draft to be good enough to send to Ram:  
    * Ralph loop needs to be fixed to actually benefit the writing of the paper.  
    * Joey needs to make the fixes Adam talked about to the gen ai acknowledgement.   
    * Joey needs to read the thesis himself and think it is good enough.   
    * Figures, screenshots  
* Have a human written summary of gen ai use in the email  
* explain that I am open to any meeting time from now to the end of quarter  
* 
