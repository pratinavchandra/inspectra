rule Data_Exfiltration_Indicators {
  meta:
    description = "Detects potential data exfiltration in Chrome extensions"
  
  strings:
    $encode1 = "btoa("
    $encode2 = "Base64.encode("
    $xhr = "XMLHttpRequest"
    $fetch = "fetch("
    $domain = /https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?/

  condition:
    (any of ($encode*)) and ($xhr or $fetch) and $domain
}
