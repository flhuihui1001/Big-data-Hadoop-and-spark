# DNSC 6920 - Big Data - Summer 2017 <br/> Prof. Marck Vaisman <br/> Assignment # 1 <br/> Due Sunday June 18, 2017 at 11:59pm <br/> 25 points


## Getting started with AWS and Hadoop

In this first assignment, you will get used to working with AWS, the command line, Hadoop and MapReduce. You will start an EMR cluster, list files, clone repositories, run a MapReduce job, put data into your cluster, and more. The tools you will be using and the skills you will be developing in this assignment are:

* Git 
* Command Line (pipes, file operations)
* SSH (logging into remote systems)
* EMR
* S3  (Fetching data, creating a bucket, storing data)
* Hadoop, HDFS, MapReduce, YARN
* Writing mapper and reducer programs in R or Python to use with Hadoop Streaming 

**Note:** You **must** use the Amazon Cloud resources to run all the code in the assignment. You may develop your mapper/reducer code locally on your laptop but the code still needs to be run on the cloud. 

## Github Classroom 

You will be using [Github Classroom](http://clasroom.github.com) for assignments. By using *git* and *Github* you will learn how to use this tool which is used for version control and should be a part of your analytics workflow. Also, I created a private repository for this course and that way your information remains private. The way it works is that by accepting the invitation to the Github Classroom that you received in your email, you will create a private repository within your Github account that is based on the repository for the problem set. Once this private repository is created in your Github account, you will be able to clone it to either your local machine as well as your cluster, and make changes to files, and submit your assignments via this way.

**Note:** It is possible that my source repository that will be cloned for you may change if there are any issues with the assignment. If they do, I need to let you know so you can sync up your repository with mine.

## Setup GitHub

Before you begin using git and Github, you will need to create a Github account if you don't already have one. Once you create your account, you will need to upload the **public ssh key** that you created for accessing your AWS resources. By adding your public ssh key to your Github account, you will be able to push changes back to the repository without having to login to GitHub.

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

### Git Tutorial

I found a very useful Git tutorial which is somewhat humorous. I think it is worth it for you to read through this tutorial: [git - the simple guide](http://rogerdudler.github.io/git-guide/).

### Using ssh agent

One thing to keep in mind is that whenever you want to use your Github repository on your cloud resources, you will need to connect to your remote machines and pass your ssh private key. This is very easy to do:

* Before you connect to your remote machine, type `ssh-add` in your terminal. You will get a confirmation that looks something like this:

```
➜  ~ ssh-add 
Identity added: /Users/marck/.ssh/id_rsa (/Users/marck/.ssh/id_rsa)
```
* You need to use the `-A` parameter in your ssh command: `ssh -A loginname@remote.machine.ip`
* To test that the ssh-agent forwarded your key to the remote machine you can test the connection to GitHub as we did before: `ssh -T git@github.com`.

### Cloning your repository

To clone your assignment repository on your local or remote machine, you need to use the following command:
`git clone git@github.com:my-repository-path/name.git`. Note: each student's repository name will be different and unique. Make sure you clone your repository from your home directory (on the remote machines) to keep things simple and will create a sub-directory within your home directory that contains the contents of your repository.

Once you clone your repository, change directories and work within the repository directory: `cd my-repository-path`.


## Practice Lab 
* Start an EMR cluster using the AWS Console with 1 master and 2 core nodes, just like we did in class.
* Once the cluster is up and running, type `ssh-add` and then ssh into the master node, remember to use the `-A` parameter `ssh -A hadoop@ip-of-master-node`. 
* Once logged on, install git on your cluster's master node: `sudo yum install -y git`
* Make sure that your ssh agent was forwarded. Test with `ssh -T git@github.com`
* Clone your repository: `git@github.com:my-repository-path/name.git`
* List the files in your cluster's HDFS (will be empty). There are two ways to do it, both are equivalent:
	* Type `hdfs dfs -ls` 
	* Type `hadoop fs -ls`
* List the files in the course S3 bucket `s3://gwu-bigdata/`. There are two ways to do this:
	* Using the [Hadoop Filesystem Shell Commands](https://hadoop.apache.org/docs/r2.8.0/hadoop-project-dist/hadoop-common/FileSystemShell.html) which also work with S3. You can list the contents of of a bucket by typing `hdfs -ls s3://gwu-bigdata/`

		```
		[hadoop@ip-172-31-76-170 ~]$ hdfs dfs -ls s3://gwu-bigdata/
		Found 3 items
		drwxrwxrwx   - hadoop hadoop          0 1970-01-01 00:00 s3://gwu-bigdata/data
		drwxrwxrwx   - hadoop hadoop          0 1970-01-01 00:00 s3://gwu-bigdata/data-gz
		drwxrwxrwx   - hadoop hadoop          0 1970-01-01 00:00 s3://gwu-bigdata/data-lzo
		```

	* Using the [AWS Command Line Interface](https://aws.amazon.com/cli/) which is installed by default on all AWS resources. This is a Python based utility.

		```
		[hadoop@ip-172-31-76-170 ~]$ aws s3 ls s3://gwu-bigdata/
                           PRE data-gz/
                           PRE data-lzo/
                           PRE data/
		```                           


## Problem 1 - Word Count, the "Hello World" of Hadoop (5 points)

In this problem, you will run a simulated MapReduce job on a small text file. I say simulated because we will not be using Hadoop to do this. 



## Problem 2 - The _quazy_ scientific instrument (10 points)

For this problem, start a 5 node 

For this problem, you will be working with various text files stored on S3 that are of in the 1-50 GB range. The files contain hypothetic measurements of a scientific instrument called a _quazyilx_ that has been specially created for this class. Every few seconds the quazyilx makes four measurements: _fnard_, _fnok_, _cark_ and _gnuck_. The output looks like this:

    YYYY-MM-DDTHH:MM:SSZ fnard:10 fnok:4 cark:2 gnuck:9

(This time format is called [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) and it has the advantage that it is both unambiguous and that it sorts properly. The Z stands for _Greenwich Mean Time_ or GMT, and is sometimes called _Zulu Time_ because the [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) word for **Z** is _Zulu_.)

When one of the measurements is not present, the result is displayed as negative 1 (e.g. `-1`). 

The quazyilx has been malfunctioning, and occasionally generates output with a `-1` for all four measurements, like this:

    2015-12-10T08:40:10Z fnard:-1 fnok:-1 cark:-1 gnuck:-1

There are four different versions of the _quazyilx_ file, each of a different size. As you can see in the output below the file sizes are 50MB (1,000,000 rows), 4.8GB (100,000,000 rows), 18GB and 36.7GB. The only difference is the length of the number of records, the file structure is the same. 

```
[hadoop@ip-172-31-76-170]$ hdfs dfs -ls s3://gwu-bigdata/data/quaz*.txt
-rw-rw-rw-   1 hadoop hadoop   52443735 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx0.txt
-rw-rw-rw-   1 hadoop hadoop 5244417004 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx1.txt
-rw-rw-rw-   1 hadoop hadoop 19397230888 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx2.txt
-rw-rw-rw-   1 hadoop hadoop 39489364082 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx3.txt
```

Your job is to find all of the times where the four instruments malfunctioned together using three different methods. The easiest way to do this is with the `grep` command. Unfortunately, as you can see, the file is *big*. There are three ways that you can filter to find the bad records:

### Part 1 - Using `grep` on its own

For this part, you will use the 4.8GB file `s3://gwu-bigdata/data/quazyilx1.txt`.

#### Method 1 - Single file on disk

In this case, you will be copying the entire file from S3 to the master node of your cluster and then you will run a grep command to find the lines that match the pattern when all four instruments fail.

1. SSH into the master node of your EMR cluster
1. Copy the file from S3 to the local filesystem of the master node 
2. Use the `time` command along with `grep` to measure how long it takes to find the lines from the file that match the pattern, and use the [Linux Pipe](http://ryanstutorials.net/linuxtutorial/piping.php) to write the filtered lines to a file called `p1a_results.txt`. 
3. Create a text file called `p1a_time.txt` where you will cut/paste the results of the `time` command.

The files to be committed to the repository for this problem are `p1a_results.txt` and `p1a_time.txt`
   
#### Method 2 - Stream file from S3 to grep   

In this case, you will "stream" the file from S3 to grep, the file does not get saved to disk. 


***Method 2*** - stream the file from S3 to your AWS VM with the AWS steaming command and use `grep` as it goes by. To stream from Amazon S3 to standard out, you use the command:

    aws s3 cp s3://<bucket>/<filename> -


### Part 2: Use Hadoop to parallelize operation (10 points)

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


## Problem 3 - Log file analysis (10 points)

The file `s3://gwu-bigdata/data/forensicswiki.2012.txt` is a year's worth of Apache logs for the forensicswiki website. Each line of the log file correspondents to a single `HTTP GET` command sent to the web server. The log file is in the [Combined Log Format](https://httpd.apache.org/docs/1.3/logs.html#combined).

If you look at the first few lines of the log file, you should be able to figure out the format. You can view the first 10 lines of the file with the command:

    aws s3 cp s3://gu-anly502/logs/forensicswiki.2012.txt - | head -10

At this point, you should understand why this command works.

Your goal in this part is to write mapper and reducer programs using Python3.4 or R with Hadoop Streaming that will report the number of hits for each month. For example, if there were 10,000 hits in January 2010 and 20,000 hits in
February 2010, your output should look like this:

    2010-01 10000
    2010-02 20000
    ...


Where `10000` and `20000` are replaced by the actual number of hits in each month.

Here are some hints to solve the problem:

* Your mapper should read each line of the input file and output a key/value pair in the form `YYYY-MM\t1` where `YYYY-MM` is the year and the month of the log file, `\t` is the tab character, and `1` is the number one.

* Your reducer should tally up the number of hits for each key and output the results.

* Once the results are stored in **HDFS**, you can output the results the `hdfs dfs -cat` command piped into a Unix sort.

1. Store the output in the file `logfile_results.txt` . 

Turn in `q4_mapper.py`, `q4_reducer.py`, and `q4_run.py` in addition to `q4_monthly.txt`.


## Submitting your assignment

Since we are using Github classroom, you will submit your assignment by "pushing" to your repo on GitHub. You will have to commit all the files that are requested (look at the Git tutorial to learn how to commit files.) After you commit, you will push your changes to your GitHub repository. I will be able to see  