var currentRow = null;

function installTrigger(){
  ScriptApp.newTrigger('onFormSubmit')
      .forSpreadsheet(SpreadsheetApp.getActive())
      .onFormSubmit()
      .create();
}


function checkIfValidEntry(){
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
  var row = sheet.getActiveRange().getRow();
  if(currentRow == row){
    return false;
  }
  return true;
}


/**
 * Sends a customized email for every response on a form.
 * 
 * @param {Object} event - Form submit event
 */
function onFormSubmit(e) {
  if(checkIfValidEntry() == true){
    var responses = e.namedValues;
    //  console.log(responses);
    
    // If the question title is a label, it can be accessed as an object field.
    // If it has spaces or other characters, it can be accessed as a dictionary.
    try{
      var timestamp = responses['Timestamp'][0];
      var email = responses['Email'][0].trim();
      var name = responses['Name'][0].trim();
      
      var status = '';
      if (responses['Email'].length > 0) {
        sendEmail(name, email);
        status = 'Email Successfully Sent';
      }
      else {
        status = 'No Email Id Present In The Form';
      }
      
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
      var row = sheet.getActiveRange().getRow();
      sheet.getRange(row, 1).setValue(name);
      sheet.getRange(row, 2).setValue(email);
      currentRow = row;
      console.log(currentRow);
      
      Logger.log("status=" + status + "; responses=" + JSON.stringify(responses));
    }
    catch(e){
      Logger.log("status= error ; responses=" + JSON.stringify({'message':e.toString()}));
    }
  }
}


function getEmailHtml(name) {
  var htmlTemplate = HtmlService.createTemplateFromFile("EmailTemplate.html");
  htmlTemplate.name = name;
  var htmlBody = htmlTemplate.evaluate().getContent();
  return htmlBody;
}


function sendEmail(name, email) {
  var htmlBody = getEmailHtml(name);
  
  MailApp.sendEmail({
    to: email,
    subject: "Google Form Filled Successfully",
    body: "Hello " + name + "this is a Confimation mail that your data was sent successfully",
    htmlBody: htmlBody
  });
}
