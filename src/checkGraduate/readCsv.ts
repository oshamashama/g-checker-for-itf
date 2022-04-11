export function readCsv(csvStr: String) {
  return convertArray(csvStr);
}

function convertArray(data) {
  const dataArray = [];
  const dataString = data.split("\n");
  for (let i = 0; i < dataString.length; i++)
    dataArray[i] = dataString[i]
      .replace(/^"/i, "")
      .replace(/"$/i, "")
      .split('","');
  return genGradeObj(dataArray);
}

function genGradeObj(array: String[][]) {
  const res = [];
  array.forEach(function (ar) {
    if (ar.length === 11 && ar[0] !== "学籍番号") {
      res.push(parseGrade(ar));
    }
  });
  return res;
}

function parseGrade(array: String[]) {
  const res = {};
  // console.log(array);
  res["course_number"] = array[2];
  res["course_name"] = array[3];
  res["credit"] = Number(array[4].replace(/ /, ""));
  res["grade"] = array[7];
  res["can_use"] =
    array[7] === "P" ||
    array[7] === "A+" ||
    array[7] === "A" ||
    array[7] === "B" ||
    array[7] === "C" ||
    array[7] === "認"; // || (array[7] === "履修中" && args.expect)
  res["used"] = false;
  res["used_rishu"] = false;
  res["isCount"] = "C0" !== array[8];
  res["type"] = array[8];
  return res;
}
