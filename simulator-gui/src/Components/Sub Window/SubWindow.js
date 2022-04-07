import React, {useState} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Stack from '@mui/material/Stack';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MoreVertIcon from '@mui/icons-material/MoreVert';
import Questionnaire from '../Question/Question';
import {TestQuestionnaire} from '../Question/Question';


import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Pagination from '@mui/material/Pagination';
import {TestNotification} from '../Notification/Notification'

export default function SubWindow(props) { // should have connection object
    
    const [currentComponent,setCurrentComponent] = useState(0)
    const [items,setItems] = useState([]);
    const [numOfItems,setNumOfItems] = useState (0)


    const isNotification = (item) => false
    const addItem = (itemToAdd) => {
      if (isNotification(itemToAdd)){
          handleIncomingNotification(itemToAdd)
      }
      else{
        const incoming_component = getComponent(itemToAdd)
        setItems(prevState =>[ itemToAdd,...prevState])
        setNumOfItems(numOfItems+1)
        if (currentComponent == 0){
          setCurrentComponent(1);
        }
      }
      
    }
    const getComponent = (itemToAdd) => {
      <TestQuestionnaire/>  //change to switch case, and parse json accordingly

    }
    const handlePaginationChange = (event,value) => {
      setCurrentComponent(value)
    }
    const handleIncomingNotification = (text) =>
    {
      toast(text, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        containerId: props.id  

        });
    }
    const styles = {
      position: 'relative',
    
    };
  return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" onClick  = {handleIncomingNotification}>
            <MoreVertIcon  /> {/* change it to fynamically */}

          </IconButton>
        }
        title={props.name}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>
        {items[currentComponent]}

        {/* <TestQuestionnaire num={20}/>   */}
        {/* <TestQuestionnaire/> */}
        <TestNotification/>
      <Pagination count={8} page={1} onChange={handlePaginationChange} size="small"/>

      </div>
        <Typography variant="body2" color="text.secondary">
        {/* <Box
      sx={{
        width: 300,
        height: 300,
        backgroundColor: '#bdbdbd',
       
      }}
    />   */}
            {/* <Questionnaire /> */}
        </Typography>


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
  );
}
