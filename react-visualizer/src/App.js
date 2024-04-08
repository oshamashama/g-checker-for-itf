import React, { useState } from "react";
import "./App.css";
import Data from "./reqJson/coins20.json";
import { readCsv } from "./checkGraduate/readCsv.ts";
import { checkGraduate } from "./checkGraduate/checkGrad.ts";
import Select from "react-select";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";

const Footer = () => {
  return (
    <footer className="footer-detail-container">
      <div className="footer-detail-container--inner center-box">
        <div className="ft">
          <a
            href="https://github.com/oshamashama/g-checker-for-itf"
            target="_blank"
            rel="noreferrer noopener"
          >
            GitHub
          </a>
        </div>
        <div>
          提供されているプログラム、またそのプログラムによる実行結果に関する保証はできかねます。
        </div>
        <div>
          選択されたファイルなどを卒業判定以外の目的に利用することはありません。
        </div>
        <div>
          当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス」を使用しています。このGoogleアナリティクスはデータの収集のためにCookieを使用しています。このデータは匿名で収集されており、個人を特定するものではありません。
          この機能はCookieを無効にすることで収集を拒否することが出来ますので、お使いのブラウザの設定をご確認ください。この規約に関しての詳細は
          <a href="https://marketingplatform.google.com/about/analytics/terms/jp/">
            Googleアナリティクスサービス利用規約のページ
          </a>
          や
          <a href="https://policies.google.com/technologies/ads?hl=ja">
            Googleポリシーと規約ページ
          </a>
          をご覧ください。
        </div>
      </div>
    </footer>
  );
};

const Table = (props) => {
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  let itemList = [];
  for (const key in props.value) {
    let pushStr =
      " " +
      (props.value[key]["now_certificated_credit_num"] === undefined
        ? 0
        : props.value[key]["now_certificated_credit_num"]) +
      "(" +
      (props.value[key]["feature_certificated_credit_num"] === undefined
        ? 0
        : props.value[key]["feature_certificated_credit_num"]) +
      ")/" +
      (props.value[key]["min_certificated_credit_num"] === undefined
        ? 0
        : props.value[key]["min_certificated_credit_num"]);
    let passed = "";
    if (
      props.value[key]["now_certificated_credit_num"] >=
      props.value[key]["min_certificated_credit_num"]
    )
      passed = "passed";
    else if (
      props.value[key]["now_certificated_credit_num"] +
      props.value[key]["feature_certificated_credit_num"] >=
      props.value[key]["min_certificated_credit_num"]
    )
      passed = "expect";
    else passed = "failed";
    console.log(props.value[key]["count_course"]);
    let count_course = "";
    for (const k2 in props.value[key]["count_course"]) {
      if (count_course === "")
        count_course += props.value[key]["count_course"][k2];
      else count_course += " / " + props.value[key]["count_course"][k2];
    }
    itemList.push([key, pushStr, passed, count_course]);
  }
  if (props.depth === 0) {
    return (
      <div className="con">
        {itemList.map(([key, st, passed, count_course]) => (
          <div>
            <div
              className={"bl_tate " + passed}
              key={key + st}
              onMouseEnter={() => {
                setHovered(true);
              }}
              onMouseDown={() => {
                setClicked(true);
              }}
              onMouseUp={() => {
                setClicked(false);
              }}
              onMouseLeave={() => {
                setHovered(false);
              }}
            >
              <p className="hight-center last-leaf">
                {!(hovered && !clicked) ?
                  (key === "" ? "" : key) + st
                  : (count_course === "" ? "該当する科目を修得していません" : count_course)}
              </p>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="con">
      {itemList.map(([key, st, passed]) => (
        <div className={"gre_yoko " + passed} key={key + st}>
          <div className={"bl_tate " + passed} key={key + st + "top"}>
            <p className="hight-center">{key === "" ? "" : key}</p>
            <p className="hight-center">{st}</p>
          </div>
          <div className={"bl_tate2 " + passed} key={key + st}>
            <Table value={props.value[key]["leaf"]} depth={props.depth - 1} />
          </div>
        </div>
      ))}
    </div>
  );
};

function Main() {
  let [JsonData, setJsonData] = useState(Data);
  let [DefJsonData, setDefJsonData] = useState(Data);
  const [, rerender] = useState();

  const onFileInputChangeCSV = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setJsonData(DefJsonData);
      checkGraduate(readCsv(reader.result), JsonData, (res) => {
        setJsonData(res);
      });
    };
    reader.readAsText(file);
  };

  const selectReq = (f) => {
    // setJsonData(DefJsonData);
    document.getElementById("inF").value = "";
    // var data = require('./reqJson/' + f.value);
    setDefJsonData(require("./reqJson/" + f.value));
    setJsonData(require("./reqJson/" + f.value));
  };

  const options = [
    { value: "cisIR20.json", label: "cisIR20(国際関係学)" },
    { value: "cisID20.json", label: "cisID20(国際開発学)" },
    { value: "math20.json", label: "math20" },
    { value: "mast20.json", label: "mast20" },
    { value: "coins19.json", label: "coins19" },
    { value: "coins20.json", label: "coins20" },
    { value: "coins21.json", label: "coins21" },
    { value: "coins23.json", label: "coins23" },
    { value: "klis21-system.json", label: "klis21(知識情報システム)" },
    { value: "klis21-knowledge.json", label: "klis21(知識科学)" },
    { value: "klis21-management.json", label: "klis21(情報資源経営)" },
  ];

  return (
    <div className="App">
      <div className="App-Upload">
        <div className="Upload-Comp">
          <label>
            twins からダウンロード(CSV/UTF-8)した
            <input type="file" onChange={onFileInputChangeCSV} id="inF" />
          </label>
        </div>
        <div className="Upload-Comp">
          <Select
            className="selectList"
            options={options}
            onChange={selectReq}
            defaultValue={{ value: "coins20.json", label: "coins20" }}
          />
        </div>
        <div className="Upload-Comp">
          <Button onClick={rerender}>判定</Button>
        </div>
      </div>
      <div className="App-main">
        <Table value={JsonData} depth={4} />
      </div>
      <Footer />
    </div>
  );
}

function App() {
  return <Main />;
}

export default App;
