import React, {useState, useEffect,useRef} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MoreVertIcon from '@mui/icons-material/MoreVert';
import Questionnaire from '../Question/Question';

import Pagination from '@mui/material/Pagination';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import MemberScreen from '../MemberScreen/MemberScreen';
import RegisterScreen from '../RegisterScreen/RegisterScreen';
export const blankUser = {"name": "", "role": "",
"sex": "", "age": -1,"id": -1};

export default function UserWindow(props) { 
    const webSocket = useRef(new W3CWebSocket('ws://127.0.0.1:7890'));
    const [userDetails,setUserDetails] = useState(blankUser)
    const changeUserDetails = (user) => {
        setUserDetails(user)
        console.log("UserWindow::changeUserDetails")
      }
    useEffect(() => {
        webSocket.current.onopen = () => {console.log("ws opened");}//ws.current.send(JSON.stringify(register));
        webSocket.current.onclose = () => console.log("ws closed");
        const wsCurrent = webSocket.current;

        return () => {
            wsCurrent.close();
        };
    }, []);
    const styles = {
        position: 'relative',
      
      };
return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={ // TODO: Change according to userDetails.role
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" >
            <MoreVertIcon  /> {/* change it to dynamically */}

          </IconButton>
        }
        title={props.name}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>

        {userDetails == blankUser? <RegisterScreen flowID={props.flowID} webSocket={webSocket.current} update_user_details={changeUserDetails}/> 
                                 : <MemberScreen webSocket={webSocket.current} user={userDetails}/>}
       
      </div>



      </CardContent>
      <ToastContainer style={styles}
  position="top-right"
  autoClose={5000}
  hideProgressBar={false}
  newestOnTop={false}
  closeOnClick
  rtl={false}
  pauseOnFocusLoss
  draggable
  pauseOnHover
  containerId={props.id}
  enableMultiContainer
  limit ={1}
/>

    </Card>
    </div>
)
}
