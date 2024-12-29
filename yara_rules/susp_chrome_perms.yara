rule Suspicious_Chrome_Permissions {
  meta:
    description = "Detects suspicious permission requests in manifest.json"
  
  strings:
    $perm1 = "\"tabs\""
    $perm2 = "\"webRequest\""
    $perm3 = "\"webRequestBlocking\""
    $perm4 = "\"<all_urls>\""
    $perm5 = "\"storage\""

  condition:
    4 of ($perm*)
}
