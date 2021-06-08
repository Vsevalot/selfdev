EML_BODIES = [
        """
From: =?windows-1251?B?yuDr6O3o7SDA7eDy7uvo6SDP4OLr7uLo9w==?=
	<sender_user@some_mail.ru>
To: "'receiver_user@some_mail.ru'" <receiver_user@some_mail.ru>
Subject: Subject
Thread-Topic: Thread Topic
Thread-Index: AdcwOP4U3xyAU1G7SyOurD2bGyhDrg==
Date: Tue, 13 Apr 2021 07:45:43 +0000
Message-ID: <f4c542824f454760b046ba39cbeceb2e@some_mail.ru>
Content-Language: ru-RU
X-MS-Has-Attach:
        """,
        """

Received: from SPB99PEXCH04.some_mail.local ([10.50.30.245]) by
 SPB99PEXCH04.some_mail.local ([10.50.30.245]) with mapi id 15.01.2242.008;
 Mon, 19 Apr 2021 10:08:42 +0300
From: =?windows-1251?B?yuDr6O3o7SDA7eDy7uvo6SDP4OLr7uLo9w==?=
	<sender_user@some_mail.ru>
To: "'receiver_user@some_mail.ru'" <receiver_user@some_mail.ru>,
	"'receiver_user@some_mail.com'" <receiver_user@some_mail.com>
CC: "'citation_user@some_mail.ru'" <citation_user@some_mail.ru>,
	=?windows-1251?B?z/Dl5OXo7SDE5e3o8SDC6+Dk6Ozo8O7i6Pc=?=
	<Predein.DV@some_mail.ru>
Subject: Subject string
Thread-Topic: Thread-topic string
Thread-Index: Adcyj8ttxfeZP8ouSDq9Y3SINICsqA==
Date: Mon, 19 Apr 2021 07:08:42 +0000
Message-ID: <2e3625cb8f0246979ae67456676f51cb@some_mail.ru>
Accept-Language: ru-RU, en-US
Content-Language: ru-RU
        """,
        """
Empty/broken data
        """
    ]


def get_sender_test_data():
    answers = [
        'sender_user@some_mail.ru',
        'sender_user@some_mail.ru',
        None
    ]
    ids = [
        'txt file',
        'eml file',
        'empty/broken'
    ]
    return EML_BODIES, answers, ids
