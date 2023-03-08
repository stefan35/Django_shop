var updateBtns = document.getElementsByClassName('update-cart')
var info_add = document.getElementById('info-message')

for(i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function () {
  var productId = this.dataset.product
  var action = this.dataset.action
  var size = this.dataset.size

  if(info_add){
    info_add.classList.remove("d-none")

    if(user == 'AnonymousUser')
      setTimeout(function(){
        addCookieItem(productId, action, size)}, 
        1000)
    else
      setTimeout(function(){
        updateUserOrder(productId, action, size)}, 
        1000)
  }else{
    if(user == 'AnonymousUser')
      addCookieItem(productId, action, size)
    else
      updateUserOrder(productId, action, size)
  }
  })
}

function addCookieItem(productId, action, size=""){
  if(action == 'add'){
    if(cart[productId] == undefined && cart[productId+size] == undefined){
      if(size != null)
        cart[productId+size] = {'quantity': 1, 'size':size}
      else
        cart[productId] = {'quantity': 1}
    }else{
      if(size != null){
        if(productId.includes(size))
          cart[productId]['quantity'] += 1
        else
          cart[productId+size]['quantity'] += 1
      }else
        cart[productId]['quantity'] += 1
    }
  }
  if(action == 'remove'){
    cart[productId]['quantity'] -= 1
    
    if(cart[productId]['quantity'] <= 0)
      delete cart[productId]
  }
    
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  window.location = window.location.href
}

function updateUserOrder(productId, action, size=""){
  var url = '/update_item/'    

  fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
    body:JSON.stringify({'productId': productId+size, "size": size, 'action': action})
  }).then((response) =>{
    return response.json()
  }).then((data) => {
    window.location = window.location.href
  });
}