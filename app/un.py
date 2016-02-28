import uncurl



print(uncurl.parse('curl https://api.sandbox.paypal.com/v1/oauth2/token  -H "Accept: application/json" -H "Accept-Language: en_US" -u "AZrccVcbcXX1BpSsTTIioUdmvL2PLwznBTkwDFEcfORpz4i_BhE6FPwiQZRfa4RD0kepGAXF5oAWoY71:EEigCPS468DFBtGYmL3WdOscFxd6O7fxOObEI8ebX3uave3flC9iXzjymdNZUli0Y3HOKRSz8WLwIejf" -d "grant_type=client_credentials"'))