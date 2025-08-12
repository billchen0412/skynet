

### Get cloudfare zone id

```sh
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>" \
  -H "Content-Type: application/json"
```

### Get cloudfare dns record id

```sh
curl -X GET "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records?name=vpn.cisc.tw" \
  -H "Authorization: Bearer <YOUR_API_TOKEN>" \
  -H "Content-Type: application/json"
```


curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer PWjrhiY6DN10L8REg-tt7UBP7rtLjHVNv558NXCq" \
  -H "Content-Type: application/json"



  

curl -X GET "https://api.cloudflare.com/client/v4/zones/e683c0f974fcc67abceb97cf5d8a8b14/dns_records?name=vpn.cisc.tw" \
  -H "Authorization: Bearer PWjrhiY6DN10L8REg-tt7UBP7rtLjHVNv558NXCq" \
  -H "Content-Type: application/json"