# Static Analysis of JS files

What to look for? 

1.Info that'll increase the attack surface\(URLs,domains etc\)  
2.Sensitive information\(Passwords,API keys,Storage etc\)  
3.Potentially dangerous areas in code\(eval,dangerously set InnerHTML etc.\)  
4.Components with known vuln \(Oudated frameworks\)  
  
**Enumerate JS files**  
1.Burp Pro &gt; Target &gt; Site map &gt; Engagement Tools &gt; FInd scripts   
  
2.use waybackurls tool 

```text
go get github.com/tomnomnom/waybackurls
waybackurls internet.org | grep "\.js" | uniq | sort
```

Then check the js file status, coz some js file no longer exist on the server anymore.

```text
cat js_files_url_list.txt | parallel -j50 -q curl -w 'Status:%{http_code}\t Size:%{size_download}\t %{url_effective}\n' -o /dev/null -sk
```

You can also use hashcheckurl.

```text
go get github.com/hakluke/hakcheckurl
cat lyftgalactic-js-urls.txt | hakcheckurl
```

  
**Making the gathered JS code readable**  
uglifyJS , JS Beautifier , JSDetox, JSNice etc....   
  
  
**Identifying interesting information in JavaScript**  
1.look for endpoints i.e full URLs,relative paths   
use relative-url-extractor , LinkFinder  
  
2.look for sensitive information   
using regex search or entropy   
regex search identify credentials   
entropy based search identify random secrets such as API keys and tokens  
  
DumpsterDiver, Repo-supervisor and truffleHog  
  
**Search for Dangerous Code in JS file**  
innerHTML elements  
eval function  
postMessage API   
window.postMessage  
window.addEventListener  
window.localStorage  
window.sessionStorage  
  
Use static security scanners such as   
JSPrime and ESLint   
  
Identify old and vulnerable JS frameworks  
Retire.js   
  
  
  
  
  
  
  
  
  
  


