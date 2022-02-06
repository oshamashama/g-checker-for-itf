
const max = 'max_certificated_credit_num';
const now = 'now_certificated_credit_num';
const min = 'min_certificated_credit_num';
const feature = 'feature_certificated_credit_num';
const count_course = 'count_course';
export function checkGraduate(grade, req, callback) {
  for (let rishu = 0; rishu < 2; rishu++)
    for (let hishu = 0; hishu < 2; hishu++)
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
              if (k4 === "必修" && hishu === 0 || k4 === "選択" && hishu === 1) {
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
                    += Math.min(rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5][now],
                      rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5][max]);
                  req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][feature]
                    += hishu * rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4]['leaf'][k5][feature];
                }
                req[k1]['leaf'][k2]['leaf'][k3][now]
                  += Math.min(rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][now],
                    rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][max]);
                req[k1]['leaf'][k2]['leaf'][k3][feature]
                  += hishu * rishu * req[k1]['leaf'][k2]['leaf'][k3]['leaf'][k4][feature];
              }
            }
            req[k1]['leaf'][k2][now]
              += Math.min(hishu * rishu * req[k1]['leaf'][k2]['leaf'][k3][now],
                hishu * rishu * req[k1]['leaf'][k2]['leaf'][k3][max]);
            req[k1]['leaf'][k2][feature]
              += hishu * rishu * req[k1]['leaf'][k2]['leaf'][k3][feature];
          }
          req[k1][now]
            += Math.min(hishu * rishu * req[k1]['leaf'][k2][now],
              hishu * rishu * req[k1]['leaf'][k2][max]);
          req[k1][feature]
            += hishu * rishu * req[k1]['leaf'][k2][feature];
        }
      }

  return req;
}

function genNow(req, rishu) {
  if (req[now] === undefined) {
    req[now] = 0;
    req[feature] = 0;
    req[count_course] = [];
  }
  return req;
}

function checkGet(grade, req, rishu) {
  const reg_name = req['leaf']['regexp_name'];
  const reg_number = req['leaf']['regexp_number'];
  for (const key in grade) {
    let flag = false;
    if (reg_name !== "") {
      const reg = new RegExp(reg_name);
      if (grade[key]["course_name"].match(reg)) {
        flag = true;
      }
    }
    if (reg_number !== "") {
      const reg = new RegExp(reg_number);
      if (grade[key]["course_number"].match(reg)) {
        flag = true;
      }
    }
    if (flag) {
      if (grade[key]["used"] === false && grade[key]["used_rishu"] === false && req[now] < req[max]) {
        if (grade[key]["can_use"] === true) {
          grade[key]["used"] = true;
          req[now] += grade[key]["credit"];
          req[count_course].push(grade[key]["course_name"]);
        } else if (grade[key]["grade"] === "履修中" && rishu) {
          grade[key]["used_rishu"] = true;
          req[feature] += grade[key]["credit"];
        }
      }
    }
  }
  return req;
}