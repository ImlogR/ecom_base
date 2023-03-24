var updateButtons= document.getElementsByClassName('update-cart')

function updateUserOrder(productId, Action){
  console.log('Transfering data')
  const data= {'productId': productId, 'action': Action};
  const options= {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data)
  };
  var url= '/update_item/'
  fetch(url, options)
  .then((Response) =>{
    if (Response.ok){
      return Response.json()
    }
    else{
      console.log("Unsuccessful")
    }
  })
  .then((data) =>{
    console.log(data)
    location.reload()
  }
)
}

function addCookieItem(productId, action){
  if(action== "add"){
    if (cart[productId]== undefined){
      cart[productId]= {'quantity': 1}
    }else{
      cart[productId]['quantity'] +=1
    }
  }
  if(action== 'remove'){
    cart[productId]['quantity'] -= 1

    if(cart[productId]['quantity'] <= 0){
      delete cart[productId]
    }
  }
  document.cookie= 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}

for(var i=0; i< updateButtons.length; i++){
  updateButtons[i].addEventListener('click', function(){
    var productId= this.dataset.product
    var action= this.dataset.action
    console.log('productId', productId, 'Action', action)

    console.log(user)
    if (user== 'AnonymousUser'){
      addCookieItem(productId, action)
    }
    else{
      updateUserOrder(productId, action)
    }
  })
}