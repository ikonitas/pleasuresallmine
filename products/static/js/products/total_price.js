$(document).ready(function(){
  $('#id_price').change(function(){
    price = parseFloat($('#id_price').val());
    margin = parseFloat($('#id_margin').val());
    get_price(price, margin)
  });

  $('#id_margin').change(function(){
    price = parseFloat($('#id_price').val());
    margin = parseFloat($('#id_margin').val());
    get_price(price, margin)
  });

  function get_price(price, margin){
    total_price = (price * margin) / 100;
    total_price = price + total_price;
    total_price = toFixed(total_price, 2);
    $('#id_total_price').val(total_price);
  }
    function toFixed(num, fixed) {
        fixed = fixed || 0;
        fixed = Math.pow(10, fixed);
        return Math.floor(num * fixed) / fixed;
    }
});
