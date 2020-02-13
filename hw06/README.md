# Homework 6

## Submission

Please see my submission in notebook `BERT_classifying_toxicity_michael_zeng_v100.ipynb`. 

The evaluation kernel can be found at https://www.kaggle.com/kernels/scriptcontent/28326965/notebook, I got prive score of 0.93539.

* P100
	- Order VSI
	
		`ibmcloud sl vs create --datacenter=wdc07  --hostname=p100a --domain=W251-zengm71.cloud --image 3651552 --billing=hourly  --network 1000 --key=1545088 --flavor AC1_8X60X25 --san`
	
		Note that the VSI flavor is a bit different than what is on the repo README.

	- Run Docker 

		`nvidia-docker run --rm --name hw06 -p 8888:8888 -d w251/hw06:x86-64`

	- Notebook
		`BERT_classifying_toxicity_michael_zeng_p100.ipynb`

* V100
	- Order VSI

		`ibmcloud sl vs create --datacenter=lon04 --hostname=v100a --domain=W251-zengm71.cloud --image=2263543 --billing=hourly  --network 1000 --key=1545088 --flavor AC2_8X60X100 --san`

	- Run Docker 

		`nvidia-docker run --rm --name hw06 -p 8888:8888 -d w251/hw06:x86-64`

	- Notebook
		`BERT_classifying_toxicity_michael_zeng_v100.ipynb`

* Comments:

	V100 is a lot faster than V100, therefore the full dataset of 1M training + .5M validation is run on V100 only. As a result, `BERT_classifying_toxicity_michael_zeng_v100.ipynb` is the notebook for finanl submission. In this notebook, 1 EPOCH AUC accuracy is 96.90% for the V100. In part 8, where I took the model trained with 1 EPOCH and continued the training for another 2, the accuracy goes up slightly to 96.98%. 
	
## Original instructions. 

**Note this is a graded homework.**
1. Read the Google Cloud Product Overview on the [TPUs](https://cloud.google.com/tpu/)  
2. Read the primer on [Bert](https://github.com/google-research/bert)  
3. Follow the below steps to run BERT in pytorch on the Jigsaw Toxicity classification dataset.  
  
### Instructions 
You will be training BERT in a jupyter notebook. Please read the below points before starting.    
* The book is set with 10K rows training and 5K rows validation - so you can test it fast in your initial development. For your final run, we would like you to train on at least 1M rows; and validate on at least 500K rows.  
* Please run it on a V100 VM and a P100 VM and report run times on training 1M rows on both. (Note, V100 will be faster, so maybe good to start there).   
* You have 8 sections found in the jupyter notebook to complete the training of BERT and answer some questions. The first 5 seem challenging - but there is a script linked in the book which should make help a lot - should be just copy and pasting the correct code chunks.   
* Your submission should be your completed notebook (either from the P100 or V100). You can submit either through a HTML or link to a private GitHub repo.   
* Please let your instructors know if it is taking an excessive amount of time. The scripts do run long on 1M rows ~ a number of hours on the both types of VM's, but the development should not take an excessive amount of time.  
* The final section in the book shows a number of tasks, you need only complete 1 of them.   
* **For turning in your work**, please send instructors the link your repo containing your completed notebooks and information on P100 and V100 runtimes etc., alternatively, mail instructors the notebooks in html format along with runtimes. 
  
  
### Start your VMs and notebook as below.  
    
Start your `ibmcloud` VM. I ran like below - note this is a P100. You will need to replace the key.   
If you use `slcli`, no need to add `--san`.  
```
ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=1418191 --flavor AC1_8X60X100 --san
```

For your v100, enter,
```
ibmcloud sl vs create --datacenter=lon04 --hostname=v100a --domain=dima.com --image=2263543 --billing=hourly  --network 1000 --key=1418191 --flavor AC2_8X60X100 --san
```

`ssh` into your machine and run the below. 
```
nvidia-docker run --rm --name hw06 -p 8888:8888 -d w251/hw06:x86-64
```
   
The above will output a `containerid` on completion, like `959f320ffed2cce68ff19d171dcd959e33ebca30a818501677978957867d96fe`
With this run the below to get your URL. 
```
docker logs <containerid>
```
  
After you run this you will get an output like below. Go into your book, replacing the public IP in the brackets. For example for the below you can go to url   `http://158.176.131.11:8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e`
```
	root@p100:~# docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/pytorch_gpu_hw06
	[I 18:46:45.371 NotebookApp] Serving notebooks from local directory: /workspace
	[I 18:46:45.371 NotebookApp] The Jupyter Notebook is running at:
	[I 18:46:45.371 NotebookApp] http://(bef46d014d15 or 127.0.0.1):8888/?token=c5d34fc988f452c4105c77a56924fe392d52991dde48478e
	[I 18:46:45.371 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

```
