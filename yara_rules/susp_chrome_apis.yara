rule Suspicious_Chrome_Extension_APIs {
  meta:
    description = "Detects potentially malicious Chrome extension API usage"
  
  strings:
    $api1 = "chrome.tabs.query"
    $api2 = "chrome.tabs.sendMessage"
    $api3 = "chrome.webRequest.onBeforeRequest"
    $api4 = "chrome.storage.sync.set"
    $api5 = "chrome.runtime.sendMessage"

  condition:
    3 of ($api*)
}
