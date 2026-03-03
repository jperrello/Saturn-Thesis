# Ten Usability Heuristics Notes

1. **Visibility of Status:** There should always be quick, appropriate feedback on what is going on in the system  
   1. This happens with saturn by showing servers show up, and the logs of registering addresses and ports when creating saturn services.  
2. **Match between sys and real world**: Follow real world conventions making things appear in a natural order, avoiding internal jargon and favoring words, phrases and concepts that are familiar to the users.  
   1. Difficult with saturn – need to investigate how i can use better language to make people understand mDNS and failover.   
3. **User Control and Freedom:** Users will often make mistakes, and therefore there needs to be a clearly marked “exit” to leave the unwanted action without having to go through an extended process.   
   1. Saturn can cut off connections to servers easily. People can join and leave wifi networks freely.  
4. **Consistency in Standards:**  Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions, as most people have expectations set from other applications they use way more (Jakob’s Law)  
   1. Saturn needs more work with this. Beacons and proxies are confusing terms. Although registering servers and endpoints are common terminology.   
5. **Error Prevention:** Good error messages are nice, but really good designs should prevent errors from happening in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action.   
   1. Saturn has this with automatically assigning host address, port number, priority, and failover  
   2. Comment on slips and mistakes. Slips are unconscious errors caused by inattention. Mistakes are conscious errors based on a mismatch between the user’s mental model and the design.  
6. **Recognition rather than Recall**: Minimize the users memory load at all times by making elements, actions, and options visible. The user should have information visible at all times and easily retrievable to prevent forgetting information in between interfaces.  
   1. I struggle to see Saturn’s connection here. Users can always run dns-sd. How do we always keep them aware of all networks?  
7. **Flexibility and Efficiency of Use**: Allow users to tailor frequent actions. Hidden shortcuts from novice users may speed up the interaction for experts, but all capabilities are still available to both novice and experts.  
   1. Saturn has the python package. Traditional API key use is still possible  
8. **Aesthetic and Minimalist Design:** Every extra unit of information on an interface will compete with relevant units of information; therefore, all interfaces should avoid containing information that is irrelevant or rarely needed.   
   1. Saturn suffers with the text records not having a consistent schema. And my whole project suffers from the special thing being  \_saturn*.\_*tcp.local  
9. **Help users recognize, diagnose, and recover from errors.** Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.  
   1. Saturn kinda doesnt do this but it is hard to see how it factors in to my project  
10. **Help and Documentation**: It is best if the system does not need any additional documentation, however it should be provided when users need to understand how to complete their tasks.  
    1. Saturn has the documentation website [https://jperrello.github.io/Saturn/](https://jperrello.github.io/Saturn/) and pypi package. 