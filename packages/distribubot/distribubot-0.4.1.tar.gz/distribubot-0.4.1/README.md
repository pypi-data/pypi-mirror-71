# distribubot

### Distribute by manual command through comments
Scans blocks for new comments containing the given comment_command. The the comment author has suffient
 token, the token account will send token to the parent author.


## Installation of packages for Ubuntu 18.04

```
sudo apt-get install python3-pip build-essential libssl-dev python3-dev
```

### Installation of python packages


```
pip3 install distribubot
```

or clone the git and install the package by
```
pip3 install beem hiveengine
git clone https://github.com/hive-engine/distribubot.git
cd distribubot
python3 setup.py install
```

#### Running
Can be running all day, will only be active when a comment with the comment_command was broadcasted.
More than one token_account and  token can be specified. Please check config.json.example.

```
$ distribubot /path/to/config.json --datadir=/datadir/ --logconfig=/root/git/distribubot/logger.json
```

|        Option       | Value                                                |
|:-------------------:|------------------------------------------------------|
| token_account | hive account name, which should distribute the token       |
| symbol   | token symbol, which should be distributed                   |
| token_memo   | memo which is attached to each token transfer               |
| reply        | when true, a reply comment is broadcasted                   |
| wallet_password | Contains the beempy wallet password |
| no_broadcast | When true, no transfer is made |
| min_staked_token | Minimum amount of token a comment writer must have |
| maximum_amount_per_comment | Maximum Amount of token that will be send at once|
| token_in_wallet_for_each_outgoing_token | Limits the amount of token a user can send every 24 hours |
| user_can_specify_amount | When true, the user can specify the amount to send up to maximum_amount, when false maximum_amount is always sent |
|default_amount | Default amount of token |
|count_only_staked_token | When True, only staked token are taken into account |
| sucess_reply_body | Reply body, when token are send|
| no_token_left_for_today | Reply body, when the user has not sufficient token in its wallet |
| fail_reply_body | Reply body, when no token are sent (not min_staked_token available) |
| no_token_left_body | Reply body, when no token are left to send |
| comment_command | Command which must be included in a comment, to activate the bot |
| usage_upvote_percentage | When set to a percentage higher than 0, the comment with the command or the receiver will be upvoted by the scot_account |
| scale_upvote_weight | When true, the upvote weight is scaled by the amount of send token |
| upvote_token_receiver | When true, the receiver is upvoted instead |


## Running the scripts
Adapt path in run-distribubot.sh
```
chmod a+x run-distribubot.sh
./run-distribubot.sh
```
or edit and copy the systemd service file to /etc/systemd/system and start it by
```
systemctl start distribubot
```