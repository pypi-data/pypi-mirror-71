### Common setup

```
% export AWS_ACCESS_KEY_ID=<IAM user with write permission to S3 bucket>
% export AWS_SECRET_ACCESS_KEY=<key for IAM user>
% export SNOWFLAKE_USER=ml_training
% export SNOWFLAKE_PASSWORD=<see Platform Analytics>
% export PYTHONPATH=$(pwd)
```

### Publish a new package

```
% git commit
% git push origin master
% ./scripts/push_version.sh
```

### Training a new model

#### Locally

1. Update version and training table name `<model config>.py` file in `bytegain/custom/cust/apartmentlist/`
2. Update file to reflect new model version and training table name
3. Run the feature analysis and create row handler
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config> --feature_analysis`
4. Tweak configuration and iterate
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config>`
5. Train the production model and upload the configuration files to S3
  * `python bytegain/custom/cust/apartmentlist/train_model.py --model_config <model config> --production`

#### On a dedicated EC2 instance

1. Ensure you have the PEM file for the EC2 instance saved in `$HOME/.ssh/vb-east.pem`.
  * If you do not have the file, you can get it from someone on the Platform Analytics team
2. If you are training with changes that are _not_ in the `master` branch on `origin`,
push your changes up to `origin` in a branch
3. If the `ml-training` instance is in the `stopped` state, it is safe to use, someone else may be
using it, so check in [#machine-learning](https://apartmentlist.slack.com/archives/CLF8TUBRT) on Slack to see if anyone else is currently using the machine.
4. Be certain you will have a reliable internet connection for the duration (up to 2 hours),
if your connection drops, training will abort.
5. Invoke `./bin/ec2_train` to start training:

```
Usage: ./bin/ec2_train <model> [-p|--prod|--production] [-f|--feature_analysis] [-b|--branch <git branch>]

  <model>                name of model config file (exists in bytegain/custom/cust/apartmentlist/)
  --branch <git branch>  git branch to use (defaults to master)
  --feature-analysis     run feature analysis on the training set
  --production           train the model and push files to S3
```
