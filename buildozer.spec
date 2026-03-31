cat > buildozer.spec << 'EOF'
[app]
title = SecurityGuard
package.name = securityguard
package.domain = org.security

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy==2.3.1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_SMS,RECEIVE_SMS,SEND_SMS,READ_PHONE_STATE,CALL_PHONE,QUERY_ALL_PACKAGES,RECEIVE_BOOT_COMPLETED

[buildozer]
log_level = 2

[android]
android.api = 34
android.minapi = 24
android.ndk = 26b
android.sdk = 34
android.gradle_dependencies = 
EOF
