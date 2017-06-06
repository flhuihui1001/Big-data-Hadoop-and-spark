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

## GitHub Classroom 

You will be using [Github Classroom](http://clasroom.github.com) for assignments. By using *git* and *Github* you will learn how to use this tool which is used for version control and should be a part of your analytics workflow. Also, I created a private repository for this course and that way your information remains private. The way it works is that you will need to accepting an invitation with a link to an assignment repository that will then create a private repository within your Github account that is based on the repository for the problem set. Once this private repository is created in your Github account, you will be able to clone it to either your local machine as well as your cluster, and make changes to files, and submit your assignments via this way.

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


**For problems 2 and 3 you can start a new cluster with 5 nodes (1 master and 4 core) or resize the cluster you started for the Practice Lab and/or Problem 1.**

## Problem 2 - The _quazy_ scientific instrument (10 points)


For this problem, you will be working with various text files stored on S3 that are of in the 1-50 GB range. The files contain hypothetic measurements of a scientific instrument called a _quazyilx_ that has been specially created for this class. Every few seconds the quazyilx makes four measurements: _fnard_, _fnok_, _cark_ and _gnuck_. The output looks like this:

    YYYY-MM-DDTHH:MM:SSZ fnard:10 fnok:4 cark:2 gnuck:9

(This time format is called [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) and it has the advantage that it is both unambiguous and that it sorts properly. The Z stands for _Greenwich Mean Time_ or GMT, and is sometimes called _Zulu Time_ because the [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) word for **Z** is _Zulu_.)

When one of the measurements is not present, the result is displayed as negative 1 (e.g. `-1`). 

The quazyilx has been malfunctioning, and occasionally generates output with a `-1` for all four measurements, like this:

    2015-12-10T08:40:10Z fnard:-1 fnok:-1 cark:-1 gnuck:-1

There are four different versions of the _quazyilx_ file, each of a different size. As you can see in the output below the file sizes are 50MB (1,000,000 rows), 4.8GB (100,000,000 rows), 18GB (369,865,098 rows) and 36.7GB (752,981,134 rows). The only difference is the length of the number of records, the file structure is the same. 

```
[hadoop@ip-172-31-76-170]$ hdfs dfs -ls s3://gwu-bigdata/data/quaz*.txt
-rw-rw-rw-   1 hadoop hadoop   52443735 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx0.txt
-rw-rw-rw-   1 hadoop hadoop 5244417004 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx1.txt
-rw-rw-rw-   1 hadoop hadoop 19397230888 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx2.txt
-rw-rw-rw-   1 hadoop hadoop 39489364082 2017-05-19 13:35 s3://gwu-bigdata/data/quazyilx3.txt
```

Your job is to find all of the times where the four instruments malfunctioned together using three different methods. The easiest way to do this is with the `grep` command. Unfortunately, as you can see, the file is *big*. There are three ways that you can filter to find the bad records:

### Using `grep` on its own

For this part, you will use the 4.8GB file `s3://gwu-bigdata/data/quazyilx1.txt`.

#### Task 1 - Single file on disk

In this case, you will be copying the entire file from S3 to the master node of your cluster and then you will run a grep command to find the lines that match the pattern when all four instruments fail.

1. SSH into the master node of your EMR cluster
1. Copy the file from S3 to the local filesystem of the master node 
2. Use the `time` command along with `grep` to measure how long it takes to find the lines from the file that match the pattern, and use the [Linux Pipe](http://ryanstutorials.net/linuxtutorial/piping.php) to write the filtered lines to a file called `p1a_results.txt`. 
3. By running the following commands, you will create a text file called `p1a_time.txt` with the results from `grep` and another file `p1a_time.txt` with the output of the time command:

```
(time grep "fnard:-1 fnok:-1 cark:-1 gnuck:-1" \
quazyilx1.txt > p2_1_results.txt ) 2> p2_1_time.txt
```
The files to be committed to the repository for this task are `p2_1_results.txt` and `p2_1_time.txt`
   
#### Task 2 - Stream file from S3 to `grep`   

In this case, you will [stream](https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-i-o-redirection) the file from S3 to grep, the file does not get saved to disk. 

```
(time aws s3 cp s3://gwu-bigdata/data/quazyilx1.txt - | \
grep "fnard:-1 fnok:-1 cark:-1 gnuck:-1" > p2_2_results.txt ) 2> p2_2_time.txt
```
The files to be committed to the repository for this task are `p2_2_results.txt` and `p2_2_time.txt`


### Use Hadoop to parallelize operation 

In this section you will parallelize the grep with [Hadoop Streaming](https://hadoop.apache.org/docs/r2.7.3/hadoop-streaming/HadoopStreaming.html).  (To see how Hadoop Streaming has been modified for Amazon Map Reducer, please review the [Amazon EMR documentation](http://docs.aws.amazon.com/emr/latest/ReleaseGuide/UseCase_Streaming.html)) Because of the minimal amount of computation done, these tasks are entirely I/O-bound. 

#### Tasks 3, 4, 5

You will run three Hadoop Streaming jobs, one for the 4.8GB file (task 3), one for the 18GB file (task 4) and one for the 36.7GB file (task 5).

In this case, our mapper program will be the `grep` tool with its parameters. The way to invoke the Hadoop Streaming Job is:

```
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
-D mapreduce.job.reduces=0 \
-D stream.non.zero.exit.is.failure=false \
-input [[input-file]] \
-output [[output-location]] \
-mapper "/bin/grep \"fnard:-1 fnok:-1 cark:-1 gnuck:-1\""
```

**What does all this mean?**

* The first line `hadoop jar /usr/lib/hadoop/hadoop-streaming.jar` is launching Hadoop with the Hadoop Streaming jar. A jar is a Java Archive file, and Hadoop Streaming is a special kind of jar that allows you to run non Java programs.
* The second line `-D mapreduce.job.reduces=0` tells the job that you want zero reduce tasks. This is a map-only job since all we are doing is filtering and not aggregating.
* The third line `-D stream.non.zero.exit.is.failure=false` is another parameter for the streaming job which tells Hadoop to not fail on task error. This is necessary in this case because Hadoop is expecting output from every map task, but since we are filtering the data the majority of the tasks will not have an output. Without this parameter, the job will fail.
* The fourth line `-input [[input-file]]` tells the job where your source file(s) are. These files need to be either in HDFS or S3. If you specify a directory, all files in the directory will be used as inputs
* The fifth line `-output [[output-location]]` tells the job where to store the output of the job, either in HDFS or S3. **This parameter is just a name of a location, and it must not exist before running the job otherwise it will fail.**
* The sixth line `-mapper "/bin/grep \"fnard:-1 fnok:-1 cark:-1 gnuck:-1\""` is the actual mapper process.

When you finish running the Hadoop Streaming jobs, you will need to extract the results from **HDFS** using `hdfs dfs -cat [[location_in_hdfs]] | sort > [[output_file]]` and create and commit three files: `p2_3_results.txt`, `p2_4_results.txt`, `p2_5_results.txt`.


## Problem 3 - Log file analysis (10 points)

The file `s3://gwu-bigdata/data/forensicswiki.2012.txt` is a year's worth of Apache logs for the [forensicswiki website](http://forensicswiki.org/wiki/Main_Page). Each line of the log file correspondents to a single `HTTP GET` command sent to the web server. The log file is in the [Combined Log Format](https://httpd.apache.org/docs/1.3/logs.html#combined).

If you look at the first few lines of the log file, you should be able to figure out the format. You can view the first 10 lines of the file with the command:

    aws s3 cp s3://gwu-bigdata/data//forensicswiki.2012.txt - | head -10

At this point, you should understand why this command works.

Your goal in this part is to write mapper and reducer programs using Python3.4 or R with Hadoop Streaming that will report the number of hits for each month. For example, if there were 10,000 hits in January 2010 and 20,000 hits in February 2010, your output should look like this:

    2010-01 10000
    2010-02 20000
    ...

Where `10000` and `20000` are replaced by the actual number of hits in each month.

There are four starter files in the repository: `logfile_mapper.py`, `logfile_reducer.py`, `logfile_mapper.R`, `logfile_reducer.R` which contain mapper and reducer shells in both R and Python. You need to modify these files to make this work.

Here are some hints to solve the problem:

* Your mapper should read each line of the input file and output a key/value pair in the form `YYYY-MM\t1` where `YYYY-MM` is the year and the month of the log file, `\t` is the tab character, and `1` is the number one.
* Your reducer should tally up the number of hits for each key and output the results.
* You will need to run the Hadoop Streaming job with the appropriate parameters (see Problem 2 for reference.)

When you finish running the Hadoop Streaming jobs, you will need to extract the results from **HDFS** using `hdfs dfs -cat [[location_in_hdfs]] | sort > [[output_file]]` and create and commit `logfile_results.txt`. 

The files to be committed to the repository for this problem are your mapper, reducer, and `logfile_results.txt`.


## Submitting your assignment

Since we are using Github classroom, you will submit your assignment by "pushing" to your repo on GitHub. You will have to commit all the files that are requested (look at the Git tutorial to learn how to commit files.) After you commit, you will push your changes to your GitHub repository. I will be able to see  

## Grading Rubric
* I will look at the results files first. If the results files are what is expected, in the proper format, sorted, etc., then you will get full credit for the problem.
* If the expected results file is not what is expected I will look at the code and provide partial credit where applicable.
* Points will be deducted for each the following reasons:
	* Instructions are not followed
	* Output is not in expected format
	* Output is not sorted
	* There are more files in your repository than need to be