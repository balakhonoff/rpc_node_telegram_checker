# rpc_node_telegram_checker
A simple telegram bot that can check an RPC node state and headlag compared to the public endpoints

Create virtual environment
```
cd ~ 
virtualenv -p python3.8 up_env  
source ~/up_env/bin/activate
```

Install
```
pip install python-telegram-bot
pip install "python-telegram-bot[job-queue]" --pre
pip install --upgrade python-telegram-bot==13.6.0  # important for compatibility

pip install numpy 
pip install web3
```

Run
```
source ~/up_env/bin/activate
python uptime_bot.py
```

Python version 3.8

Screenshots:


*If everything is fine*
![If everything is fine](https://i.ibb.co/Fnp0Csj/Screenshot-2023-06-29-at-15-37-25.png)

*If the node is lagging*
![If the node is lagging](https://i.ibb.co/FbBCX1d/Screenshot-2023-06-29-at-15-53-58.png)



