# damp-permifrost-concatinator

## Introduction
The DAMP dataplatform utilises Terraform for the majority of infrastructrue.
However permisions are managed using a tool Called Permifrost.
This is a open source tool created by the people at gitlab.
It simplifies the setup of the permissions for users and accsess within Snowflake.

One of the challanges with Permifrost however is that it does not support the creation of multiple files.
That is to say that all Permissions need to be stored in a singel file for a given Permifrost run.

Another is that while it is technically possible to have multiple runs of permifrost within the same Snowflake account,
These instances need to be entirely insulated form one another.
That is to sa that roles from one instance cannot be repeated in another file.

For our desing utilising a central run of permiforst to create a RBAC based
Accsess and functional role structure, that acts as a full tree, this is a
problem. We ended up with a massive file that quicklly became hard to parse.
The RBAC design with default roles for read and write seoeraty created a
considderable amount of boiler plate code that contrbuted to the file bloat,
but did not add any additional information.

In order to solve these challanges the Permifrost Concatinator was created.
The purpose of the application is to suport the splitting of Permifrost files
into multiple files while also remowing some of the unneccecary boiler plate
Access role code.

## How does the app work? 
The Permifrost concatinator austensibly reads the files in the directory it is
pointed at and translates them to an internal representation of what roles,
databases, warehouses, and users should exist. 

If called to do so it will run the verification steps against this
representation. As all objects are python primitives this process is rellativly
fast. 

Based on the verificatin and the internal representation we can then start
genetaing the "missing" access roles (AR) that have purposfully been left out
of the initial files, as they represented the boiler plate roles. These roles
are generated into the internal representation of the structure.

In order to generate the final file that is handed off to Permiforst is using
simple text generation class that has been configured with Permifrost
spessific indentation. Permifrost is very particular on its inndentation and
does not follow the YAMEL standard perfectly by requireing certain objects to
be at spessific inndentations. This neccesitated the creation of the custome
text generator. 

The file is finally writen back to the filesystem where it is picked up by
Permifrost itsef. 


### The plan stage
In an attempt to provide additional transparency to what changes occure in any
given run a basic Plan stage was added to the app. This stage compares the
current ineternal state to a previouse state, and prints a formated list of
changes. 

This neccesitated the abbility to store state from one run to the next. However
the app is purpusfully buildt to be a momoryless, shortlived system. Thus the
state needed to be stored in an external location. At the current point of
development that state storage is a ´json´ dump of the interal representation
of the system. 

This dump is sendt to the filesystem, and later read from the file system in
the same fassion as the role spessification files themselvs. This is a large
and cumbersome fil, but is not intended for human consumption. 

It is possibe that this file can grow to sizes larger than what is supported
as storage on GitHub, and as such shoud have a longterm storrage not in the
same location as the code itself. There also is a known bug where when runing
the concatinator within a PR and GitHub Actions atempting to write the updated
state file back to the branch of the PR might fail, causing the state to
outdated upon the next run, reporting additional changes, than the ones
acctually being proposed. 

As this feature is only used as a sanity check on PRs and has no impact on the
actual chages, it has not been a priority to change it. The best solution for
the bug is the same as a neccecary change in anticipation of sate file
increase. Move the file after it is written out of the filesytem, and load it
in prior to running the plan stage. This behaviour is the same pattern that
Terraform uses. However the conctinator is not buildt to communicate with a
backend the way Terraform is. The same effect can however be achieved using
GitHub Actions to move the file in and out of the alternate storrage.
