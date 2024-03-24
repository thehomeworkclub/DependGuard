# DependGuard
Our Project for the 2024 CrackTheCode Hackathon @ Concordia University

DependGuard is a powerful tool designed to enhance the security of your GitHub projects by analyzing dependencies and providing valuable insights. With DependGuard, you can ensure that your project's dependencies are up-to-date, secure, and free from vulnerabilities. DependGuard is aimed at improving the usability and user experience involved with OSS (open source softwares).

## **THE PROBLEM:** 
Many open source softwares have a key issue; since the software isn't extremely profitable, there may not be enough or support in the community behind the software. Using outdated packages expose vulnerabilities that can range from a small error in coding to a complete compromise of the software and its users.

For example, there is a known vulnerability in the Django package from 1 week ago. Since Django handles complex web tasks such as creating frameworks and databases, this could have compromised many websites on the internet. Such websites could have been dealing with critical sensitive information, such as personal details of their users. Although it was not a serious vulnerablity in the package, it still proves that this issue is a very real reality even for large softwares with large communities. This issue's severity and magnitude increases exponentially when there is a smaller community and a smaller number of users.

## **STATEMENT OF PURPOSE:**
Our software wishes to address critical cybersecurity flaws that can be observed in the current OSS community.

## **FEATURES**
- Dependency Analysis: DependGuard thoroughly examines your project's dependencies, identifying potential security vulnerabilities.
- Security Insights: Receive detailed reports on vulnerabilities found in your project's dependencies, along with recommendations for remediation.
- Ease-of-use: The website is an ad-hoc tool that is all hosted on a website. The use of DaisyUI enables it to have a modern design while being just as effective. It is an all-in-one tool that allows for both github link entries and requirements.text (accepts many other file types). It identifies the community score, the dependency score, and many other statistics. If a vulnerability is found, all known fixes in the community are provided on the website.
- Privacy: There is no data collected on the user and everything is entirely open source. It does not need to be installed on the user's device in order to function.
- Universality: We use multilpe APIs and databases to create a functional project that covers everything AND MORE that other existing solutions use. 

## **HOW ARE WE UNIQUE?**
One of the most direct comparisons of our project to an existing one is called DependaBot. It automatically creates pull requests to update repositories when a new one is available but it fails to have basic cybersecurity elements. 
Blackduck finds vulnerabilities but it won't tell you how active the community is. Our project isn't a static code analyzer like black duck. It's meant to provide all the information possible, and expose underlying issues like in transitive dependencies that Blackduck may not detect. Our project is exclusively open source and costs nothing to open source users, enabling and improving the open source community. 

## **STEPS TO USE:**
1. Access the webpage
2. Upload a github link or a specific file specifying repositories and packages needed
3. Submit this to the website for processing
4. Look at the results and fix vulnerabilities found
