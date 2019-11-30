`Still in development`
# Automatically spin the coin at [ChronoGG](https://www.chrono.gg/)
ChronoGG website has a cool feature that allows you to click a coin in their homepage (you can do this every 6h-24h) and receive a currency(coins) from it. 

After a few times of doing this you will have accomulate enough coins to then exchange for a free game in their [coin shop](https://www.chrono.gg/shop) page. 

And I am all about free games but I don't like repeating the same process over and over again when it can be automated... And that's why I made this!

## What it is
This is a simple python3.7 lambda function that will use your account [JWT token]() to spin the wheel at [ChronoGG](https://www.chrono.gg/) which in turn will accumulate and allow you to exchange this for free games .

## Getting started
Personally I avoid hosting such processes on my machine so I don't have to worry about having it turned ON during the times when it's supposed to run and this is a very small a quick process so I though it would be a perfect fit for an AWS Lambda function!

To deploy the code you will have to first create an AWS lambda function. 

Note that the makefile has the lambda function name hardcoded as `chronogg-auto-spin` but you can change it to have the name of yours.

And only then you can run:
```
make deploy
```

Now you need to obtain your account JWT token and feed it to the lambda function as an environment variable. To do that follow the steps:
- navigate to https://www.chrono.gg/
- login into your account
- open the developer tools in your browser (press F12) and go to the network tab
- hover the mouse over your email on the top right corner of the page and select `coins`
- filter the list of methods results on your developer tools window (you can type `coins` in the textbox
- click in the second one and search the headers of the request for the token. It's format is `JWT yo83fsdlkSAsdjfsoiDLKklsdiJ9.eyJlbWFpbCI6InJpY2FyZG9vc29yaW8uZ2FtZXNAZ21haWwuY29tIiwisdks83QiOiJib3Rsb2tpIiwidWlkIjoiNWIyMDJmOTk2OTFmODMwMDEzOWJksdkj723DKA3djac0NTA2MzY0LCJleHAiOjE1Nzk2OTAzkSjsd9zOi8vd3d3Lksdkjfsdf223ImlzcyI6Imh0dHBzOi8vYXBpLmNocm9uby5jlsdf2382JSmp0aSI6ImI5ZmVmMzlhMzIyZDQ0kjddzk1ZTg5NWY2OTc2MGE3In0.XrArg5v6r5Fnsd7347BD8UA73jdskh29fat_kZr3CrqYRyfga`

Copy this value (including the `JWT` part) into a new environment variable of the lambda named `JWT_TOKEN`

Finally you can trigger your function either manually or by cloudwatch events!

## Recommendation
You can setup an virtual env before running either `make build` or `make deploy` (which will trigger the build when run) with virtualenv. 
If you need to install it, run the following (for linux/macos):
```
python3 -m pip install --user virtualenv
```
And then create a new virtual env named `chronogg` in your current directory with:
```
virtualenv chronogg
```

A version of the `build` rule of the makefile which uses a virtual env named `chronogg` is:
```
build:
	mkdir -p package && \
	source chronogg/bin/activate && \
	pip3 install -t ./package requests && \
	deactivate && \
	cd package && \
	zip -r9 main.zip . && \
	mv main.zip .. && \
	cd .. && \
	zip -g main.zip main.py
```
