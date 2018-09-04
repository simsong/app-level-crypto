// Utility functions used to convert strings to/from binary arrays
function ab2str(buf) {
   var bufView = new Uint8Array(buf);
   return String.fromCharCode.apply(null, bufView);
}

function str2ab(str) {
   var buf = new ArrayBuffer(str.length);
   var bufView = new Uint8Array(buf);
   for (var i=0, strLen=str.length; i<strLen; i++) {
      bufView[i] = str.charCodeAt(i);
   }
   return buf;
}

// Make window.crypto browser nuetral
window.crypto = window.crypto || window.msCrypto; //for IE11
if (window.crypto.webkitSubtle) {
   window.crypto.subtle = window.crypto.webkitSubtle; //for Safari
}

function makeReadyToSend(enc) {
   return encodeURIComponent(btoa(ab2str(enc)));
}

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

   // Function 'data_encrypt' encrypts '_buff' using provided '_key' and '_meth'
   function encrypt_buffer(_fld, _buff, _key, _meth) {
      var data = {};

      // start encryption. If success, return encoded encrypted value
      // if failure, write a message to the browser JavaScript console
      return window.crypto.subtle.encrypt(_meth, _key, _buff).then(
         function(result) {
            data[_fld] = makeReadyToSend(result);
            return data;
         },
         function(err) {
            messageAndFade("Encryption Error see log");
            console.log("encrypt_json.js: error in "+_meth+" encryption:", err);
         }
      );
   }

   messageAndShow("Encrypting Form Data");
   
   // Import JWK public key
   var imp_proc = window.crypto.subtle.importKey( "jwk", jwk, { name: "RSA-OAEP", hash: {name: "SHA-256"}}, false, ["encrypt"] );
   
   // Wait for 'importKey' proc to finish
   imp_proc.then(function(key) {
      window.rsakey = key;

      // Generate AES initialization vector
      window.aesiv = window.crypto.getRandomValues(new Uint8Array(16));

      // Generate AES CBC Session Key
      // TODO: Use AES GCM when it's available in pycrypto
      window.crypto.subtle.generateKey({ name: "AES-CBC", length: 128 }, true, ["encrypt", "decrypt"]).then(
         function(key) {
            window.aeskey = key;

            // Build JSON string of form values
            var json = JSON.stringify( { 'firstname': $('#firstname').val(), 'age' : $('#age').val() } ); 
            var buff = makeReadyToEncrypt(json);

            // Encrypt JSON string return a promise of a result 
            return encrypt_buffer('json', buff, window.aeskey, { name: "AES-CBC", iv: window.aesiv }).then(
               function(result) {
                  return result;
               }
            );
         },
         function(err) {
            messageAndFade("Generate AES Key error see log");
            console.log("generateKey: "+err);
         }
      ).then(
         function(result) {
            var data = result;

            // Export AES key so it can be encrypted
            window.crypto.subtle.exportKey("raw", window.aeskey).then(
               function(keydata) {
                  console.log('keydata', new Uint8Array(keydata));

                  // Array to hold all encryption promises
                  var proc = new Array();

                  proc.push(encrypt_buffer('keydata', keydata,       window.rsakey, { name: "RSA-OAEP" }));
                  proc.push(encrypt_buffer('iv',      window.aesiv,  window.rsakey, { name: "RSA-OAEP" }));
            
                  // Wait for ALL promises in the array to finish:
                  Promise.all(proc).then(
                      // Merge results into one & send to receiver
                      function(results) {
                         //var data = window.data;
                         $.each(results, function( index, value ) {
                            data = $.extend(data, value);
                         });
                         console.log('data', data);
                         $.get(receiver, data,
                            function(result) {
                               console.log(result);
                               messageAndFade("Thank You "+$("#firstname").val());
                               // Clear form
                               $("#firstname").val('');
                               $("#age").val('');
                            });
                      }
                  );
               },
               function(err) {
                  console.log("exportKey", err);
               }
            );
         }
      );
   });
}

$(document).ready(function() {
    $("#message").hide();
});

