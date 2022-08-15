#!/bin/zsh

MODE=$(gum choose "dev" "prod" --limit=1 || echo "dev")
CMD=$(gum choose "run.sh" "redeploy.sh" --limit=1 || echo "run.sh")
for i in $(gum choose --no-limit 9 100 200 300 400 500 600)
do
  gum style --foreground 103 --border-foreground 212 --border double \
            --align center --width 50 --margin "1 2" --padding "2 4" \
            "Running with $i pods"

  sed "s/%REPLICAS%/$i/g; s/%MODE%/$MODE/g" deploy/my-scheduler-temp.yaml > deploy/my-scheduler-deploy.yaml 
  sed "s/%REPLICAS%/$i/g; s/%MODE%/$MODE/g" deploy/my-controller-temp.yaml > deploy/my-controller-pod.yaml 

  # make does not work, we need to wait for the controller a bit 

  # CMD="run.sh"
  ./script/$CMD

  mt=200
  st=$(( i > mt ? i : mt ))
  gum spin -s line --title "waiting for algorithm to complete, sleeping for $st seconds" \
     sleep $st

  gum style --foreground 212 "writing results to data-${i}pods.json"
  ./script/getmetrics.py ${i}

done
