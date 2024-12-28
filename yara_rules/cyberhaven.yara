rule Cyberhaven_Extension_Pattern {
    meta:
        description = "Detects suspicious messages seen in the Cyberhaven attack"
        severity = "high"

    strings:
        $msg1 = "action:" wide ascii
        $rtext1 = "-rtext" nocase wide ascii
        $rtext2 = "_rtext" nocase wide ascii
        $rjson1 = "-rjson" nocase wide ascii
        $rjson2 = "_rjson" nocase wide ascii
        $errors1 = "-check-errors" nocase wide ascii
        $errors2 = "_check-errors" nocase wide ascii

    condition:
        $msg1 and
        (any of ($rtext*)) and
        (any of ($rjson*)) and
        (any of ($errors*))
}
