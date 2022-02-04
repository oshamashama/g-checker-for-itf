
const max = 'max_certificated_credit_num';
const now = 'now_certificated_credit_num';
const min = 'min_certificated_credit_num';
const feature = 'feature_certificated_credit_num';
export function checkGraduate(grade, req, callback) {
  // console.log(req);
  // console.log(grade);
  for (let rishu = 0; rishu < 2; rishu++)
    for (const k1 in req) {
      req[k1] = genNow(
        req[k1],
        rishu
      );
      for (const k2 in req[k1]['leaf']) {
        req[k1]['leaf'][k2] = genNow(
          req[k1]['leaf'][k2],
          rishu
        );
        for (const k3 in req[k1]['leaf'][k2]['leaf']) {
          req[k1]['leaf'][k2]['leaf'][k3] = genNow(
            req[k1]['leaf'][k2]['leaf'][k3],
            rishu
          );
          for (const k4 in req[k1]['leaf'][k2]['leaf'][k3]['leaf']) {
            req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4] = genNow(
              req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4],
              rishu
            );
            for (const k5 in req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf']) {
              req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5] = genNow(
                req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5],
                rishu
              );
              req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5] = checkGet(
                grade,
                req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5],
                rishu === 1
              );
              req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][now]
                += rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5][now];
              req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][feature]
                += rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5][feature];
            }
            req[k1]['leaf'][k2]['leaf'][k3][now]
              += rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][now];
            req[k1]['leaf'][k2]['leaf'][k3][feature]
              += rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][feature];
          }
          req[k1]['leaf'][k2][now]
            += rishu * req[k1]['leaf'][k2]['leaf'][k3][now];
          req[k1]['leaf'][k2][feature]
            += rishu * req[k1]['leaf'][k2]['leaf'][k3][feature];
        }
        req[k1][now]
          += rishu * req[k1]['leaf'][k2][now];
        req[k1][feature]
          += rishu * req[k1]['leaf'][k2][feature];
      }
    }

  return req;
}

function genNow(req, rishu) {
  // if (req[now] === undefined) {
  if (rishu === 0) {
    req[now] = 0;
    req[feature] = 0;
  }
  return req;
}

function checkGet(grade, req, rishu) {
  // req[now] += 10;
  // console.log(req);
  const reg_name = req['leaf']['regexp_name'];
  const reg_number = req['leaf']['regexp_number'];
  // console.log(reg_name)
  // console.log(reg_number)
  for (const key in grade) {
    let flag = false;
    if (reg_name !== "") {
      const reg = new RegExp(reg_name);
      if (grade[key]["course_name"].match(reg)) {
        flag = true;
      }
      // console.log(":")
    }
    if (reg_number !== "") {
      const reg = new RegExp(reg_number);
      if (grade[key]["course_number"].match(reg)) {
        flag = true;
      }
      // console.log(":")
    }
    if (flag) {
      //     if not kamoku.used:
      // console.log("---" + reg_name + "regregreg" + reg_number);
      // console.log("---" + grade[key]["course_name"] + "/" + grade[key]["credit"]);
      if (grade[key]["used"] === false && grade[key]["used_rishu"] === false) {
        if (grade[key]["can_use"] === true) {
          grade[key]["used"] = true;
          req[now] += grade[key]["credit"];
          // req[now] += grade[key]["credit"];
          // req[now] += grade[key]["credit"];
        } else if (grade[key]["grade"] === "履修中" && rishu) {
          grade[key]["used_rishu"] = true;
          req[feature] += grade[key]["credit"];
          console.log(rishu);
          console.log(grade[key]["course_name"]);
        }
      }

      //         if kamoku.can_use:
      //             kamoku.used = True
      //             res_credit += kamoku.credit
      //             res_course_name.append("{}{}{}".format(Color.GREEN, kamoku.course_name, Color.RESET))
      //         elif kamoku.grade == "履修中":
      //             kamoku.used = True
      //             feature_credit += kamoku.credit
      //             res_course_name.append("{}{}{}".format(FEATURE_COLOR_STR, kamoku.course_name, Color.RESET))
      //         else:
      //             if args.drop:
      //                 res_course_name.append("{}{}{}".format(Color.RED, kamoku.course_name, Color.RESET))
    }

  }
  return req;
}