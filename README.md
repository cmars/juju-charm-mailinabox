# Overview

From the [Mail-in-a-Box project homepage](https://mailinabox.email):

>Mail-in-a-Box lets you become your own mail service provider in a few easy
>steps. It’s sort of like making your own gmail, but one you control from top to
>bottom.
>
>Technically, Mail-in-a-Box turns a fresh cloud computer into a working mail
>server. But you don’t need to be a technology expert to set it up.

# Usage

Before deploying mailinabox, you'll need to obtain a public domain name,
`yourdomain.email` for example. Give your new deployment a hostname like
`box.yourdomain.email`, and deploy with:

    juju deploy cs:~cmars/trusty/mailinabox
    juju set-config mailinabox hostname=box.yourdomain.email
    juju expose mailinabox

Once mailinabox is installed and running, open a browser to
https://box.yourdomain.email/admin and follow the directions there to complete
setup.

## Fallback

If mailinabox fails to obtain a Let's Encrypt certificate, you'll need to
browse to https://public-ip/admin and follow the directions to obtain the
necessary TLS certificates manually.

## Known Limitations and Issues

The generated admin password is currently worse than the kind of password an
idiot would put on his luggage. Not ready for general use yet.

This charm is not designed to "scale". mailinabox is primarily intended as an
all-in-one standalone personal email server. If you wanted something else,
mailinabox (and this charm) probably aren't for you. Adding units will probably
do unexpected, undesirable things.

mailinabox currently installs haveged, which I disagree with.

# Contact Information

No support is provided for this charm. By using this charm, you assume full
responsibility for, and familiarity with what it does. Read the source.

For assistance with the upstream project after installation, see
https://mailinabox.email.

# License

   Copyright 2016 Casey Marshall

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
