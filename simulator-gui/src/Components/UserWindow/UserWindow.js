import React, {useState, useEffect,useRef} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import PersonIcon from '@mui/icons-material/Person';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MoreVertIcon from '@mui/icons-material/MoreVert';

import Pagination from '@mui/material/Pagination';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import RegisterScreen from '../RegisterScreen/RegisterScreen';
import Questionnaire from '../Question/Question';
import UserNotification from '../UserNotification/UserNotification';
import TestNotification from '../TestNotification/TestNotification';
import TestDataEntry from '../TestDataEntry/TestDataEntry';
export const blankUser = {"name": "", "role": "",
"sex": "", "age": -1,"id": -1};

export default function UserWindow(props) { 
    const webSocket = useRef(null)
    const [userDetails,setUserDetails] = useState(blankUser)
    const [items,setItems] = useState([]);
    const [currentComponent,setCurrentComponent] = useState(0)
    const [numOfItems,setNumOfItems] = useState (0)
    useEffect(() => {
        webSocket.current = new W3CWebSocket('ws://127.0.0.1:7890');
        webSocket.current.onopen = () => console.log("ws opened");
        webSocket.current.onclose = () => console.log("ws closed");
        webSocket.current.onmessage = (message)=>addItem(JSON.parse(message.data))
        return ()=>{
         console.log("UNMPUNT") //unMount Code
        }    }, []);

        useEffect(()=>console.log(currentComponent),[currentComponent])

    useEffect(()=>{
      setNumOfItems(items.length)
      if(currentComponent >= items.length){
          items.length==0? setCurrentComponent(0) : setCurrentComponent(1)
        }
      if( items.length>0 & currentComponent <=0){
        setCurrentComponent(1)
      }
    },[items])
    const handlePaginationChange = (event,value) => {
      setCurrentComponent(value)
    }
  
    const sendRegister  = (registerDetails) =>
    {
      console.log("UserWindow::sendRegister ~~ registerDetails: " + JSON.stringify(registerDetails))

      var register_request = {...registerDetails}
      register_request["type"] = "register"
      register_request["workflow"] = props.workflow_id  
      webSocket.current.send(JSON.stringify(register_request))
      setUserDetails((prev)=>(registerDetails))
    }
    const styles = {
        position: 'relative',
      
      };
    const sendData = (object_to_send) =>{
        object_to_send.id = userDetails.id   
        object_to_send.workflow_id = props.workflow_id     
        dismiss_current()
        webSocket.current.send(JSON.stringify(object_to_send))
      }
    const dismiss_current = ()=>
    {
      console.log("UserWindow::dismiss_current ")

      let newArr = [items];
      newArr.splice(currentComponent-1,1)
      setCurrentComponent((currentComponent) => (currentComponent-1))
      setItems(newArr)
    }
      const isNotification = (item) => false

    const addItem = (itemToAdd) => {

      console.log("UserWindow::addItem ~ " + JSON.stringify(itemToAdd))
      if (isNotification(itemToAdd)){
      }
      else{
        if(isComponent(itemToAdd)){
          setItems((prevState) =>([...prevState,itemToAdd]))
        }
        }
      }  

      const getComponent = (itemToAdd) => {
        // return (<TestNotification test={1}/>)
        switch(itemToAdd["type"]) {
          case "questionnaire":
    
            return (<Questionnaire questionnaire = {itemToAdd} send ={sendData}/>)
            case "notification":
            return (<UserNotification notification = {itemToAdd["text"]} dismiss = {dismiss_current}/>)
            case "test":
              return (<TestNotification test_notification = {itemToAdd} dismiss = {dismiss_current}/>)
            case "test data entry":
              return (<TestDataEntry test_data_entry = {itemToAdd} send ={sendData}/>)
          default:
            console.log("User::getComponent::default block ~ "  +JSON.stringify(itemToAdd))
            // code block
        } 
        // <TestQuestionnaire/>  //change to switch case, and parse json accordingly
    
      }
    
       const isComponent = (message) => {
        const valid_types = ["questionnaire","notification"]  
        
    
          return valid_types.includes(message["type"])
      }

      const handle_delete = ()=>{
        webSocket.current.close()
        props.delete(props.id)
      }
return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={ // TODO: Change according to userDetails.role
          <PersonIcon>
            
          </PersonIcon>
        }
        
        action={
          <IconButton aria-label="settings" onClick={handle_delete} >
            <MoreVertIcon /> {/* change it to dynamically */}

          </IconButton>
        }
        title={userDetails.name + props.id}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>

        {userDetails == blankUser? <RegisterScreen sendRegister={sendRegister}/> 
                                 :  <div>
                                 {currentComponent>0? getComponent(items[currentComponent-1]): undefined}
                        
                        
                              <Pagination count={numOfItems} page={currentComponent} onChange={handlePaginationChange} size="small"/>
                        
                            </div>}
       
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
