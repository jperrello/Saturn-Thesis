  
Abstract  
This abstract should provide a general overview of each section of Saturn. It should first explain the protocol itself, then our approach to integrating it, then lastly, our evaluation results. It should acknowledge the security flaws as well, and how we discuss each of these things. 

Introduction:  
Our too cheap to meter argument is a good attention grabber. We should open with that, but in a way that makes sense. We should acknowledge that that quote comes from a different time period and in a different academic space, energy. We want to say that we're taking the idea of too cheap to meter and instead putting that to AI services.

Explain that Joey, the author, originally had this idea because he wanted to provision AI access to everyone on campus for the reasons we explain in our motivations. ​​The intro is the primary argument for why the paper needs to exist, so we should also explain what we end up contributing (in a slightly different way then we did in the abstract

Background  
What service discovery exists and why didnt we use them. Basically where a lot of our academic work fits in:  
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

**Explain why we chose Saturn over these methods**   
Most content in background section is about mDNS but you have less space for each of these above things 

Design:

```
Design ( these arent hardcoded sections but what should be covered:
  Goals (what is the design of saturn acheiving, not the project itself but architecture)
  Audiences ( who uses Saturn)
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

Implementation:  
This is the section where we explain what Saturn was implemented into. Things like the VLC extension or the router or open code Saturn. Rather than just creating sections for each of these individual implementations, I want you to explain how this project progressed because we had a date. We started with the VLC extension in order to show that with Saturn, AI could be integrated into apps that are not AI native.

VLC is an extension that plays media. We wanted to show that with Saturn, an app that currently never had AI in it could now have AI services within it. The router was shown to prove that we could provision AI on a network level. Everyone who was connected to the router would be able to use the same Saturn services.

That was the point behind the router and we could describe how this router was made in order to achieve that goal. Lastly, you could talk about the open code implementation. The open code implementation was used to show how Saturn could be integrated into coding agents. Coding agents are more complex than just chat-based applications because there's things like tool calling and back and forth conversation and editing files and remembering knowledge of a code base.

We wanted to show that all of that was possible still if you used Saturn. Acknowledge that open code is natively AI based and therefore some developers may want to write off Saturn by thinking it is just AI focused. But I want to remind you that we made the VLC extension to show that your app doesn't necessarily have to be core AI based.

It could be focused on something else. You just want to add AI to that app. 

Evaluation:  
The evaluation is where we talk about our three claims and how we prove them. We don't only talk about these claims in isolation, but we also talk about how they relate to our initial motivations of the Saturn paper that was described in the introduction. These evaluation claims in a way are there to prove that Saturn works and benefits society and is worth configuring on a larger scale. 

Discussion:  
Discussion could be thought of the what happens now section. Think about now that Saturn has been invented and it's been proven, what does this mean for the world? In my opinion, this means that universities could now allow students who want to use AI services to directly connect to an endpoint and be charged solely based off the amount of tokens they are using.

The university then doesn't have to pay for large enterprise subscriptions, but rather could set aside money for an AI budget that then is used for students to access AI services. This also means that in the future, if Saturn becomes widely adopted enough, a lot of apps no longer would even have to worry about setting up API keys or worrying about configuration on that end, because it is just assumed that people probably have a Saturn server running if they are using an AI service. Additionally, Saturn may lower the barrier of entry for people to get into AI because they don't have to spend money on the service to experiment with it. And they may just casually walk upon an AI service because an app decided to implement it when they didn't before. The user had no idea that that service is inherently AI because behind the scenes, AI was happening on the network without them thinking about it. 

Conclusion:  
The conclusion should only be about what the reader has read in the paper. Explain what Saturn contributed one more time. Explain the things we proved, why Saturn exists, and why it's important. Explain that future directions could go some way and some other way.

And explain the primary motivation of the authors one last time. Conclusion will probably end up being one short paragraph. 