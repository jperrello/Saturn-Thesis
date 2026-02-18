Saturn: Zero-configuration AI Discovery  
**Joey Perrello**   
December 12, 2025

	In 1954 Lewis Strauss, chairman of the US Atomic Energy Commission, coined the phrase: “too cheap to meter,” a prediction that atomic energy would eventually produce electricity so abundant and inexpensive that it wouldn't be worth the cost of metering individual usage. At the time, this was a response to the broader optimism surrounding nuclear power in the early atomic age. I see a similar broad optimism to generative artificial intelligence (GenAI) today. Coca-Cola is introducing AI generated ads,[^1] chatbots are being used in every subject of higher education[^2], and app developers are scrambling to put AI features into their systems.[^3] Yet, the cost of AI is nowhere close to being “too cheap to meter.” Most mainstream chatbot services require $20 monthly subscriptions,[^4] and enterprise tiers are even steeper,[^5] with OpenAI's newest model, o1-pro, costing $150 per million input tokens.[^6] Beyond the expense, provisioning accounts and distributing access keys is difficult. Each app might require its own API key, and larger organizations often need separate keys per department or user just to track costs. Open source developers struggle with this; they might want to add AI features to their applications but cannot justify forcing users to bear API costs or subscription complications.  
	My work introduces Saturn, a service designed to restructure this fragmented infrastructure. Rather than requiring every application and consumer to pay separately, Saturn moves access to AI services to the network level. Saturn is a zero-configuration service discovery system that uses multicast DNS and DNS service discovery to automatically advertise and locate OpenAI-compatible AI backend services on a local network without manual endpoint configuration. A household, university, or office can set up Saturn servers once, and everyone on that network gets access, managed by network administrators. A parallel to draw from is connecting to a printer via Bonjour: users press “Print,” and the protocol handles finding the printer and transmitting the document. Saturn applies this same workflow for AI.  
	Existing work in zero-configuration AI remains limited,[^7] though the idea itself is not new. Requests to implement similar functionality have appeared in the Ollama community, but none gained traction. Open WebUI[^8] offers a zero-configuration mechanism, but it requires running the Ollama LLM inference services on the same machine. Most work related has focused on application-level LLM routing in projects like LiteLLM and Requesty, which direct user prompts to appropriate models to reduce API costs rather than solving the discovery problem. I struggled to find any implementation as extensive as Saturn for AI service discovery.   
	Saturn servers encapsulate all configuration for an AI service.  They query model providers’ endpoints, for example, an OpenRouter Saturn server requests available models from the /v1/models endpoint. The servers also handle all requests and response parsing from cloud or local LLM provider’s chat/completions endpoint. Most importantly, Saturn servers use DNS-SD to register themselves on the local network under the \_saturn.\_tcp.local service type. Servers do not contain logic related to user prompts, or application-specific behavior; they just offer AI services. In practice, Saturn servers are the responsibility of IT administrators to integrate on their LAN. Clients, by contrast, are created by application developers who want to use Saturn. All clients share the same purpose: discover Saturn servers and store their routing information. Discovery can be accomplished by using OS-specific mDNS commands, or language-specific packages like Zeroconf in Python. After Saturn servers are discovered, the client can be any application that wants AI capabilities. I have built implementations such as a proxy client to Jan[^9] that enables a traditional chat UI, a VLC[^10] extension that roasts user’s media taste, and an OpenWebUI function that allows users to chat with discovered models immediately upon launching the interface.  
	With Saturn, I have established the foundation for zero-configuration AI discovery: servers that advertise themselves via mDNS, clients that discover providers automatically, and working integrations that demonstrate the concept in real applications. Saturn addresses what prior efforts left unsolved or ignored, and allows anyone on a network to have access to AI services without subscriptions or pre-provisioned API keys.

[^1]:  [https://futurism.com/artificial-intelligence/coke-ai-holiday-ad](https://futurism.com/artificial-intelligence/coke-ai-holiday-ad) 

[^2]:  [https://longreads.com/2025/05/21/chatgpt-ai-college-cheating/](https://longreads.com/2025/05/21/chatgpt-ai-college-cheating/) 

[^3]:  [https://www.zoom.com/en/products/ai-assistant/](https://www.zoom.com/en/products/ai-assistant/)

[^4]:  [https://openai.com/index/chatgpt-plus/](https://openai.com/index/chatgpt-plus/) 

[^5]:  [https://claude.com/pricing/max](https://claude.com/pricing/max) 

[^6]:  [https://platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing) 

[^7]:  [https://github.com/ollama/ollama/pull/751](https://github.com/ollama/ollama/pull/751) 

[^8]:  [https://github.com/open-webui/open-webui](https://github.com/open-webui/open-webui) 

[^9]:  [https://www.jan.ai/](https://www.jan.ai/) 

[^10]:  [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/) 