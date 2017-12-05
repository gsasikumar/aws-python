# aws-python

This is a simple python library that helps to run my docker based services with route 53 registration and service discovery.

So the idea is to auto register every service to route 53 with a unique name. The naming convention is service_name<counter>.example.domain.com. The script will autodetect the name based on a port check.

Environment Variables
-----------------------
AWS_ACCESS_KEY = #AWS ACCESS KEU

AWS_SECRET_KEY = # AWS SECRET KEY

SERVICE_NAME = # Service name eg: "kafka" this will result in the script registering kafka1.domain.com

HEALTH_CHECK_PORT = #A port that we could use to connect and check if the service with the given name is working If it works we will not allocate that name.

DOMAIN_NAME = #hosted zone name Do not use the . at the end.

To Run
-----------------------
auto_register_service.py

Make this script as your entrypoint script in aws

License
-----------------------
Copyright (c) 2017, gsasikumar@gmail.com
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the organization nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.