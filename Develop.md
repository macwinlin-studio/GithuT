<div align="center">
  <img src="https://s1.imagehub.cc/images/2022/04/09/favicon.png" width="100px" height="100px">
  <h1 align="center">Develop Other GithuT?</h1>
  
  Only Have English Version
  
  <a href="https://github.com/macwinlin-studio/GithuT/blob/1.0.0/LICENSE">
    <img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="">
  </a>
  <a href="https://www.microsoft.com/en-us/windows">
    <img src="https://img.shields.io/badge/platform-windows-orange" alt="">
  </a>
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-v3.9-orange" alt="">
  </a>
</div>

If you try to develop other version,please contact [githut@macwinlin.ml](mailto:githut@macwinlin.ml)!

## Version

### GitHub Tools GUI Application

If you try to develop GUI application,please use this project's core.But you can use other cores,too.

And if you use our core,please contact [githut@macwinlin.ml](mailto:githut@macwinlin.ml)!

And if your(or your team's) project is very fantastic,we will add your project to official GUI application list(will write author).

### GitHub Tools Shell Application

This application want to rewrite?

OK,if you want to rewrite shell,[contact us](mailto:githut@macwinlin.ml)!

**But unofficial shell application's probability of joining official is small.**

### GitHub Tools Language Core

Really,we want Language Core to include more languages.

~~So you can modify language core and publish to anymore!~~

After [22w30a](https://github.com/macwinlin-studio/GithuT/releases/tag/22w30a), please don't change language core to add new language. Please make a language package.

Simplified Chinese language package from MacWinLin Studio CGK Team.

Now use `config language zh-cn` in GithuT 22w30a and after, language core will get Simplified Chinese from GitHub Pages.

#### How to make a language package?

First, we want two JSON files: *all-language.json* and *info.json*

*all-language.json*'s text like this:

```json
{"backup":{"key":"text","key":"text"},"update":{"key":"text","key":text"},"main":{"key":"text","key":"text"}}
```

*key* is variable name, and *text* is translated text.

---

*info.json*'s text like this:
```json
{"name":"GitHub Tools ??? Language Package","date":"modify time","author":"your team name","website":"githut.macwinlin.ml","language":"??-??"}
```

Then you can put files to your web server to start server, or share to others.

##### Why not use .zip file?

Why we not use *.zip* file to make language package, like backup file?

Oh, I want to use *.zip* file, too. But at 22w30a finished, we are testing, but at Python Package ZipFile extracting *.zip* file, program report an error. It can't extracting Unicode word, so we not use *.zip* file to make language package.

##### So why not use .tar file?

*.zip* can't use, we see another file:*.tar* file. But we don't know how to extract *.tar* or *.tar.gz* file, and 22w30a snapshot is finished, we use 5 days to make others function, now is Thursday, if we don't published, 22w30a will become 22w31a.

We are don't update this project 5 weeks, 22w25a is newer version before 22w30a.

Maybe we will use *.tar* or *.tar.gz* file after.

### GitHub Tools Main Core

Why modify main core?Because you want to develop GUI application?OK!

**But unofficial shell application's probability of joining official is small.**

**The probability is smaller than Shell**

Please know,main core's update time maybe very fast,so please update your main core fast too.

Maybe it's a little update,only modify one line code.

You can add more function in your core.

Maybe your application is good!Better than ours!

### GitHub Tools Backup Core

You can rewrite this core.

But please use this mode to make backup file,then this file can use in our version,too!

#### Step 1:

e.g. Database:

![Database](https://s1.imagehub.cc/images/2022/05/01/Snipaste_2022-05-01_15-14-23.jpg)

Then the backup file is a compressed file(suffix is *.zip*)

--------

A backup file:

backup-0000-0-00-000000<i>.backup</i>(original suffix is *.zip*)

|-backup-0000-0-00-000000.json

|-backup-0000-0-00-000000.sha256

#### Step 2

Make these two files.

*backup-0000-0-00-000000.json*'s text is:

```json
{"ver": 1.0, "data": ["zh-cn", 0, "123456", 0, 0]}
```

And *backup-0000-0-00-000000.sha256*'s text is:

**7b6ad5b57789578e5b5a39af262adb278197b5a795e4dd7c64be488fb4f43502**

Yes,*.sha256* file's text is *.json*'s SHA256 value.

#### Step 3

Then change compressed file's suffix to *.backup*.

In the end,the backup file's name is **_backup-0000-0-00-000000.backup_**(backup-*yyyy*-*mm*-*dd*-*random number(100000-1000000)*.backup

## Maintainers

This project's maintainers are MacWinLin Studio CGK Team's member.

## License

You can select any open source license!
