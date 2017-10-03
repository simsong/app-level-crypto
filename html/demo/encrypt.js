
// Utility functions used to convert strings to/from binary arrays
function ab2str(buf) {
   var bufView = new Uint8Array(buf);
   console.log('enc ', bufView);
   return String.fromCharCode.apply(null, bufView);
}

function str2ab(str) {
   var buf = new ArrayBuffer(str.length);
   var bufView = new Uint8Array(buf);
   for (var i=0, strLen=str.length; i<strLen; i++) {
      bufView[i] = str.charCodeAt(i);
   }
   console.log(str, bufView);
   return buf;
}

// Make window.crypto browser nuetral
window.crypto = window.crypto || window.msCrypto; //for IE11
if (window.crypto.webkitSubtle) {
   window.crypto.subtle = window.crypto.webkitSubtle; //for Safari
}

// TODO: Fix this to match decryption server side script
function makeReadyToSend(enc) {
   return encodeURIComponent(btoa(ab2str(enc)));
}

// TODO: Test str2ab functions properly
function makeReadyToEncrypt(str) {
   return str2ab(str);
}

function messageAndShow(msg) {
   $("#message").html(msg);
   $("#message").show();
}

function messageAndFade(msg) {
   messageAndShow(msg)
   $("#message").fadeOut(3000);
}

// The Main Function
function sendEncrypted(event, jwk, receiver) {

   // Don't allow the form to submit
   event.preventDefault();

   if (($("#firstname").val() == "") || ($("#age").val() == "")) {
      messageAndFade("Please complete form");
      return false;
   }

   // Function 'encrypt' encrypts '_fld' string value using provided '_key'
   function survey_field_encrypt(_fld, _key) {
      var data = {};
      var buff = makeReadyToEncrypt($("#"+_fld).val());

      // start encryption. If success, set data[] to be a key/value pair
      // if failure, write a message to the browser JavaScript console
      return window.crypto.subtle.encrypt( { name: "RSA-OAEP" }, _key, buff).then(
         function(result) {
            data[_fld+"Encrypted"] = makeReadyToSend(result);
            return data;
         },
         function(err) {
            messageAndFade("Encryption Error see log");
            console.log("encrypt.js: error in RSA-OAEP encryption:", err);
         }
      );
   }
   
   messageAndShow("Encrypting Form Data");

   // Import JWK public key
   var imp_proc = window.crypto.subtle.importKey( "jwk", jwk, { name: "RSA-OAEP", hash: {name: "SHA-256"}}, false, ["encrypt"]);
   
   // Wait for 'importKey' proc to finish
   imp_proc.then(function(key) {

      // proc is an array of encryption promises, each one encrypts a separate field
      var proc = new Array();
      
      // Start crypto for each field.
      proc.push(survey_field_encrypt('firstname', key));
      proc.push(survey_field_encrypt('age',       key));
      
      // Wait for ALL promises in the array to finish:
      Promise.all(proc).then(
         // Merge results into one & send to receiver 
         function(results) {  
            var data = {};
            $.each(results, function( index, value ) {
               data = $.extend(data, value);
            });
            
            console.log('data', data);
            // Send results back to receiver in a GET request
            $.get(receiver, data,
                function(result) {
                    messageAndFade("Thank You "+$("#firstname").val());
                    // Clear form
                    $("#firstname").val('');
                    $("#age").val('');
                });
      });
   },
   function(err) {
       messageAndFade("Import Key error see log");
       console.log("importKey: "+err);
   });
}

$(document).ready(function() {
    $("#message").hide();
});

