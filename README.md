# DNSC 6920 - Big Data - Summer 2017 <br/> Assignment # 1 <br/> Due Sunday June 18, 2017 at 11:59pm


## Getting started with AWS and Hadoop

In this first assignment, you will get used to working with AWS and other command line stuff. You will start an EMR cluster, list files, clone repositories, run a MapReduce job, put data into your cluster, and more. The tools you will be using in this 
* Git (command line)
* SSH (making keys and logging in to remote systems)
* AWS (creating VMs)
* S3  (Fetching data, creating a bucket, storing data)
* Hadoop, HDFS, MapReduce

**Note:** The code has only been tested on MacOS and Linux. If you are using Windows, we recommend that you exclusively solve the homework in a virtual machine at Amazon, and that you only use your Windows computer for logging in to the remote server.


## Github Classroom 

You will be using [Github Clasroom](http://clasroom.github.com) for assignments. By using *git* and *Github* you will learn how to use this tool which is very useful for version control and should be a part of your analytics workflow. Also, I created a private repository for this course and that way your information remains private. The way it works is that by accepting the invitation to the Github Classroom that you received in your email, you will create a private repository within your Github account that is based on the repository for the problem set. Once this private repository is created in your Github account, you will be able to clone it to either your local machine as well as your cluster, and make changes to files, and submit your assignments via this way.


## Setting up GitHub

Before you begin using git and Github, you will need to create a Github account if you don't already have one. Once you create your account, you will need to upload the **public ssh key** that you created for accessing your AWS resources. By adding your public ssh key to your Github account, you will be able to push changes back to the repository without having to logig to GitHub.

* Login to your GitHub account and go to "Settings"
* In the "Settings" area, select "SSH and GPG keys"
* Click on "New SSH key"
* Create a title for your key (the name is whatever you want - just as in AWS)
* Copy the contents of your `id_rsa.pub` file into the "Key" box
* Once you do this, you can test that your ssh key works with GitHub by opening a Terminal and typing `ssh -T git@github.com`. If you are successful, you will see a message like this:

```bash
➜  ~ ssh -T git@github.com
Hi wahalulu! You've successfully authenticated, but GitHub does not provide shell access.
```

### Using ssh agent

One thing to keep in mind is that whenever you want to use your Github repository on your cloud resources, you will need to connect to your remote machines and pass your ssh private key. This is very easy to do:

* Before you connect to your remote machine, type `ssh-add` in your terminal. You will get a confirmation that looks something like this:
```bash
Identity added: /Users/marck/.ssh/id_rsa (/Users/marck/.ssh/id_rsa)
```
* You need to use the `-A` parameter in your ssh command: `ssh -A loginname@remote.machine.ip`
* To test that the ssh-agent forwarded your key to the remote machine you can test the connection to github as we did before: `ssh -T git@github.com`.

### Cloning your repository

To clone your assignment repository on your local or remote machine, you need to use the following command:
`git clone git@github.com:my-repository-path/name.git`. Note: each student's repository name will be different and unique. and make sure you do it from your home directory.


## Practice Lab (not graded)

* Start an EMR cluster using the AWS Console with 1 master and 2 core nodes, just like we did in class.
* Once the cluster is up and running, type `ssh-add` and then ssh into the master node, remember to use the `-A` parameter `ssh -A hadoop@ip-of-master-node`. 
* Once logged on, install git on your cluster's master node: `sudo yum install -y git`
* Make sure that your ssh agent was forwarded. Test with `ssh -T git@github.com`
* Clone your repository: `git@github.com:my-repository-path/name.git`

### 




For the following problems, we will be working with various text files stored on S3 that are of in the 1-100GB range. The file contains hypothetic measurements of a scientific instrument called a _quazyilx_ that has been specially created for this class. Every few seconds the quazyilx makes four measurements: _fnard_, _fnok_, _cark_ and _gnuck_. The output looks like this:

    YYYY-MM-DDTHH:MM:SSZ fnard:10 fnok:4 cark:2 gnuck:9

(This time format is called [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) and it has the advantage that it is both unambigous and that it sorts properly. The Z stands for _Greenwich Mean Time_ or GMT, and is sometimes called _Zulu Time_ because the [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) word for **Z** is _Zulu_.)

When one of the measurements is not present, the result is displayed as negative 1 (e.g. `-1`). 

The quazyilx has been malfunctioning, and occasionally generates output with a `-1` for all four measurements, like this:

    2015-12-10T08:40:10Z fnard:-1 fnok:-1 cark:-1 gnuck:-1

Your job is to find all of the times where the four instruments malfunctioned together. The easy way to do this is with the `grep` command. Unfortunately, as you can see, the file is *big*. We have stored the file in Amazon S3. There are three ways that you can filter to find the bad records:

***Method 1*** - copy the file to your AWS VM (slow!) and use
   `grep`. (If you need to count, you can also use `wc`). 

***Method 2*** - stream the file from S3 to your AWS VM with the AWS steaming command and use `grep` as it goes by. To stream from Amazon S3 to standard out, you use the command:

    aws s3 cp s3://<bucket>/<filename> -

***Method 3*** - Use Hadoop running on one or more VMs to search the file in parallel, with each Hadoop worker starting at a different point.

## Question 3

First, make sure that you are able to run `aws` commands on your instance by trying to list the contents of the course S3 bucket `s3://gu-anly502/`. Below we use the `aws s3 ls` command to do that:

	[ec2-user@ip-172-31-52-185 A1]$ aws s3 ls s3://gu-anly502/
	                           PRE A1/
	                           PRE gutenberg/
	                           PRE maxmind/
	2016-03-05 14:21:58       1150 bootstrap-.bashrc
	2016-03-21 02:58:57       2735 bootstrap.sh
	2016-03-05 02:18:43       1237 startup.sh
	[ec2-user@ip-172-31-52-185 A1]$

In this question we will work with the 4.8GB file `s3://gu-anly502/A1/quazyilx1.txt`.

Determine the amount of time that Method 1 takes by copying the file `s3://gu-anly502/A1/quazyilx1.txt` from S3 to your instance VM and reporting the amount of time that it takes to do the copy operation, the amount of time to takes to do the scan, and the total number of lines that indicate a malfunction. Store this in a file called `q3.txt`. Your file should have this format:

    # download and serch to a t2.nano instance
    source: s3://gu-anly502/A1/quazyilx1.txt   # should be proper S3 URL
    date: 2016-02-04T10:10:10                   # Date, in ISO-8601 time
    mode: download
    download: 100                               # in seconds
    search: 200                                 # also in seconds
    malfunctions: 42                            # in lines

(Of course, the numbers will be different in your case.) If you are interested, this file is in [YAML](http://yaml.org/) format. The information after the `#` are comments and ignored.

## Question 4

Determine the amount of time that Method 1 takes by streaming the file from S3 to your VM and reporting the amount of time that the search takes and the number of lines indicating a malfunction. Perform the streaming by using the `aws s3 cp` command and copying from the S3 URL to the device `-`, and then piping the result into a `grep` process.

Store your report in a file called `q4.txt`. Your file should have the format:

    # streaming to a t2.nano
    date: 2016-02-04T10:10:10   # Date, in ISO-8601 time
    mode: streaming
    streaming: 150 
    malfunctions: 42 

Now, add your files to your local repository, push the changes to your git server, and shut down your VM. 

Extra credit (1 point): Create a program called `streaming-time.py` which performs this benchmark automatically. Your program should take two parameters: the source URL and the destination filename. A skeleton program has been provided.

## Question 5

Create a t2.large instance and repeat the streaming exercise. Store the results in a file called `q5.txt` the results:

    # streaming to a t2.large
    date: 2016-02-04T10:10:10   # Date, in ISO-8601 time
    mode: streaming 
    streaming: 150
    malfunctions: 42

## Question 6

Finally, we want you to give us a list of the malfunction entries. You will place them in a file and store that file on S3. Place the malfunction entries in a file called `q6-malfunctions.txt`.


## ANLY 502 Assignment 2: Learning MapReduce (V1.4)

## Required skills and technologies

* YARN
* Hadoop
* MapReduce

In this assignment you will learn the basics of MapReduce. You will do this with four exercises: 

1. We will rework the filtering exercise of [Assignment 1](../A1/Readme.md) on Hadoop MapReduce using Hadoop's "Streaming"API. We will do this with a _mapper_ that filters out the lines that are not wanted, and a _reducer_ that simply copies from input to output.
2. We will then perform the classic "word count" exercise, which creates a histogram of all the words in a text document. The mapper will map single lines to individual words, and the reducer will count the number of words.
3. We will perform a logfile analysis, using web logs from from the website [https://forensicswiki.org/](https://forensicswiki.org/) between TKDATE and TKDATE. We will generate a report of the number of web "hits" for each month in the period under analysis.
4. We will then introduce the concept of the _combiner_, which is a reducer that runs on each mapper before the keys are combined globally. We will use the combiner to implement an efficient "top-10" pattern that computes the top-10 on each node, minimizing the amount of data that is transfered.

## Part 1: Creating your first EMR cluster.

1. If you VMs from Assignment #1 are still running, log into them and make sure that the git repositories are committed and pushed back to your git server.  (Be sure to use `git status` to see if there are any files that need to be added to the git repository with `git add`.)
2. Log into the [Amazon Web Services console](https://aws.amazon.com/) and make sure that your prevous VMs are shut down. 
3. Log into the [Elasitic Map Reduce console](https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1#) and create a cluster. Below we walk you through the "Quick options."

* Log to S3
* Create a cluster for Core Hadoop.
* Use m3.xlarge with 3 instances (1 master and 2 core nodes)
* Use your existing EC2 key pair (hopefully you still have access to the private key!)

4. Click on `AWS CLI export` and copy the command line into the file [q1.txt](q1.txt) in this directory.  Answer the questions in the file.
5. Log into the head end node ssh. Note: *git* will not be installed on the EMR cluster, but *python 3.4* is installed by default!  (We just discovered this, and we're thrilled!)
6. Run the command `df -h` to see the drives attached to your virtual machine. 
7. Review the [YARN Commands](https://hadoop.apache.org/docs/r2.7.3/hadoop-yarn/hadoop-yarn-site/YarnCommands.html) on the Apache Hadoop website.  Run the `yarn version` command to see which version of YARN you are using. Run the `yarn node -list` comkmand to see the nodes that are installed on your cluster. 

*Yea! You are now ready to use MapReduce!*

## Part 2: Basic Filtering with Map Reduce

In this section we will replicate the filtering project of Assignment #1, but we'll do it with [Hadoop Streaming](https://hadoop.apache.org/docs/r2.7.3/hadoop-streaming/HadoopStreaming.html).  (To see how Hadoop Streaming has been modified for Amazon Map Reducer, please review the [Amazon EMR documentation](http://docs.aws.amazon.com/emr/latest/ReleaseGuide/UseCase_Streaming.html)) Because of the minimal amount of computation done, these tasks are entirely I/O-bound. 

We have given you a program called [run.py](run.py). This Python program is specially created for this course. It both runs the Hadoop Streaming job and writes time results into a data file. There is also a symbolic link to `run.py` called [p2_python.py](p2_python.py). When you run the command `p2_python.py`, it will default to using the program `q2_mapper.py` as the mapper and `q2_reducer.py` as the reducer, but you can change these with the `--mapper` and `--reducer` arguments. The program uses `--input` to specify the input S3 file/prefix, or HDFS file/directory.  The `--output` option specifies where the output is stored.  You can specify other things as well; use `python34 run.py --help` to get a list of the options.

We have also give you two starting Python programs: [q2_mapper.py](q2_mapper.py) and [q2_reducer.py](q2_reducer.py). These programs implement _wordcount_. You need to change them to implement a filtered counting!

1. Run a Hadoop Streaming job using a modified version of the provided [q2_mapper.py](q2_mapper.py) and [q2_reducer.py](q2_reducer.py) that  outputs the number of lines that have the `fnard:-1 fnok:-1 cark:-1 gnuck:-1` pattern. The input to the Hadoop Streaming job is an S3 filename. 

You can run the Hadoop Streaming job two ways:

* Using the provided [run.py](run.py) Python script as explained above, or,

* Manually running the `hadoop` command as explained in class using the following as an example: 

```
hadoop jar /usr/lib/hadoop/hadoop-streaming-2.7.3-amzn-1.jar \
-files q2_mapper.py,q2_reducer.py \
-input [[input-file]] -output [[output-location]] \
-mapper q2_mapper.py \
-reducer q2_reducer.py
```

2. Run the program on the file `s3://gu-anly502/A1/quazyilx1.txt` and verify that you get the same result that you got in Assignment 1. 

3. Run the program on the file `s3://gu-anly502/A1/quazyilx2.txt`, a 19.4GB file, and note the answer.

4. Run the program on the file `s3://gu-anly502/A1/quazyilx3.txt`, a 39.5GB file, and note the answer.

5. You did the above problems with your cluster with 1 master node and 2 core nodes. The master node controls your cluster, hold HDFS files, and can run jobs. The core nodes holds HDFS files and run jobs. Amazon's EMR allows you to dynamically add (or remove) core and task instances. As you add more core and task instances, your jobs will run faster, up to a particular point.  Add a core node and recompute the amount of time it takes to run the job on `quazyilx1.txt`, `quazyilx2.txt` and `quazyilx3.txt`.

6. Repeat the experiment with 2 and 4 Task nodes. The prototype [run.py](run.py) program that we have given you computes the clock time that the job took and records the number of nodes in an output file. We have also created a symbolic link called [q2_python.py](q2_python.py) that points to [run.py](run.py). When the [q2_python.py](q2_python.py) link is given to the Python language, the [run.py](run.py) sees the name that it has been called with and stores the results in a file called [q2_results.txt](q2_results.txt). The `--plot` option of the program should read this file and plots it using [matplotlib](http://matplotlib.org/). However, currently it doesn't. Instead, there is a program called [grapher.py](grapher.py) that generates a plot with fake data that is hard-coded into the file. We will modify the program to do the plotting by the end of the first weekend of the problem set, but you can do it yourself if you wish the experience! To use this program, you will need to either install matplotlib on your head-end, or else you will need to commit the results to your private git repository, pull the results to a system that has matplotlib installed, and generate the plot there. Turn in the files `q2_results.txt`, `q2_plot.png` and `q2_plot.pdf`, showing how the speed of this system responds to increases in the number of nodes.

## Part 3: HDFS

As in Part 2, these steps are entirely I/O bound. However this time you are able to control the I/O performance of your system.

1. Resize your cluster and remove all of the Task nodes.  You now have 3 nodes: 1 master and 2 core.

2. Copy the file s3://gu-anly502/A1/quazyilx3.txt to your local HDFS system.

3. The program [q3_python.py](q3_python.py) is another link to the program (run.py)[run.py] but stores its results in the file [q3_results.txt](q3_results.txt). Run the program and compute how long it takes to run.

4. When you copied the file `quazyilx3.txt` to your HDFS system, it was split into blocks and stored on three different systems. Delete the file in HDFS and resize your cluster so that it has 5 Core nodes.  Copy the file `quazyilx3.txt` back to your HDFS system; now it will be stored on 6 nodes (the 1 master and the 5 core nodes).  Re-run [q3_python.py](q3_python.py) and see how the time that the program takes changes.

5. Delete the file `quazyilx3.txt` again, resize your cluster to have 10 Core nodes, copy the file `quazyilx3.txt` back to your cluster, and re-run [q3_python.py](q3_python.py). This determines how long the process takes with the file stored on 11 HDFS nodes.

Commit your results to your git repository and push the repository to your git server. Shut down your cluster when you are done.

Turn in the file `q3_results.txt`, which should include the results of all of your experimental runs.

## Part 4: Logfile analysis

The file s3://gu-anly502/logs/forensicswiki.2012.txt is a year's worth of Apache logs for the forensicswiki website. Each line of the log file correspondents to a single `HTTP GET` command sent to the web server. The log file is in the [Combined Log Format](https://httpd.apache.org/docs/1.3/logs.html#combined).

If you look at the first few lines of the log file, you should be able to figure out the format. You can view the first 10 lines of the file with the command:

    aws s3 cp s3://gu-anly502/logs/forensicswiki.2012.txt - | head -10

At this point, you should understand why this command works.

Our goal in this part is to write a map/reduce programs using Python3.4 and Hadoop Streaming that will report the number of hits for each month. For example,
if there were 10,000 hits in the month January 2010 and 20,000 hits in
the month February 2010, your output should look like this:

<pre>
    2010-01 10000
    2010-02 20000
    ...
</pre>

Where `10000` and `20000` are replaced by the actual number of hits in each month.

Here are some hints to solve the problem:

* Your mapper should read each line of the input file and output a key/value pair in the form `YYYY-MM\t1` where `YYYY-MM` is the year and the month of the log file, `\t` is the tab character, and `1` is the number one.

* Your reducer should tally up the number of hits for each key and output the results.

* Once the results are stored in in HDFS, you can output the results the `hdfs dfs -cat` command piped into a Unix sort.

1. Store the output in the file `q4_monthly.txt` . 

Turn in `q4_mapper.py`, `q4_reducer.py`, and `q4_run.py` in addition to `q4_monthly.txt`.

## Part 5: EXTRA CREDIT Finding the top-10 hits
In this final exercise, you will generate a bar graph of the top-10 hits. To do this, you will need to  create two map-reduce jobs:

* Job #1 will read the entire logfile and output a list of each URL and the total number of hits.

* Job #2 will read the file that includes each URL and the top number of its, and extract the top 10.

* Finally, you will then plot the bargraph. You'll want to do that with matplotlib. Although you might be tempted to have the plotting take place as part of the mapreduce jobs, it's better to have the mapreduce jobs store results in an intermediate file and have a separate program that does the plotting.

You may find this easier to do with the `MRJOB` framework discussed in class L03 than with Hadoop streaming.  

* Modify the Makefile and add the files and plot results.

* Be sure to turn in a file called q5_explaination.txt that explains how you solved this problem.

This problem is worth another 20%.

## Make submit and submit!

As before, you should submit a single ZIP file. Please use the `Makefile` and the `validator.py` to make the Makefile. Do this by typing `make submit`. Be sure to edit `../user.cfg` to put in your personal information.


