
// To avoid refreshing the entire page by updating price 
$(function update_values() {
    // send asynchronous HTTP GET (AJAX) requrest to the route /getprice that return data from server as JSON 
    $.getJSON($SCRIPT_ROOT+"/getprice",
        function(productlist) {
            // format numbers as currency strings
            let dollarUSLocale = Intl.NumberFormat('en-US');

            // loop through JSON object
            for (var i = 0; i < productlist.length; i++)
            {
                // update and format the html corresponding contet
                if (productlist[i].currentprice !== null && productlist[i].pricediff !== null)
                {
                    $("#currentprice" + productlist[i].id).html('$' + dollarUSLocale.format(productlist[i].currentprice))
                    $("#pricediff" + productlist[i].id).html('$' + dollarUSLocale.format(productlist[i].pricediff))
                }
                
                
                $("#status" + productlist[i].id).html(productlist[i].status)
                
                    
            }
            try
            {
                console.log("Get request successful!")  
            }
            catch(err)
            {
                console.log('Request failed', error);
            }
            
        });
        
    // fetch data every 120 seconds
    setTimeout(arguments.callee, 120000);
});

