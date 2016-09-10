const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const wordObjSchema = new Schema({
  text: String,
  link: String
});

const wordObj = mongoose.model('WordObj', wordObjSchema);
module.exports = wordObj;