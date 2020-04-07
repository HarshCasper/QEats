curl -X POST -H 'Authorization: Key 3bd9b90143524facba8d87ae9f57aac8' -H "Content-Type: application/json" \
    -d '
    {
      "inputs": [
        {
          "data": {
            "image": {
              "url": "https://recipes.timesofindia.com/thumb/54308405.cms?imgsize=510571&width=800&height=800"
            }
          }
        }
      ]
    }' \
    https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs
