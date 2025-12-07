const fs = require('fs');
const appJson = JSON.parse(fs.readFileSync('app.json', 'utf8'));

// Fix package name
if (appJson.expo.android && appJson.expo.android.package) {
  appJson.expo.android.package = 'com.sams.attendance';
  console.log('✅ Changed package from "' + appJson.expo.android.package + '" to "com.sams.attendance"');
}

fs.writeFileSync('app.json', JSON.stringify(appJson, null, 2));
console.log('✅ Updated app.json');
