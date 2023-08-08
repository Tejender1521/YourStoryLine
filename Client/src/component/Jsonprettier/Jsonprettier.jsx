
import "react-json-pretty/themes/1337.css";
import React from "react";
import JSONPretty from "react-json-pretty";


const JOSNP = (props) => {
 return (
      <div className="root">
        {/* <pre className="pre">{JSON.stringify(this.props.data, null, 2)}</pre> */}
        <JSONPretty
          data={props.data}
          space="4"/>
      </div>
    ); 
}

export default JOSNP
