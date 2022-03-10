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
import Question from '../Question/Question';



export default function SubWindow(props) { // should have connection object
    const [state,setState] = useState(1);
    
    const [currentComponent,setCurrentComponent] = useState(null)
    
    const [itemsQueue,setItemsQueue] = useState([]);
    
    const isNotification = (item) => false
    const addToQueue = (itemToAdd) => {
      if (isNotification(itemToAdd)){
          handleIncomingNotification(itemToAdd)
      }
      else if (currentComponent != null){
          setItemsQueue(prevState =>[ itemToAdd,...prevState])
        }
        else
        {
          // currentComponent = g
        }
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
        console.log()
    }
    const styles = {
      position: 'relative',
    
    };

  return (
    <div>
    <Card sx={{ maxWidth: 345 }}>
      <CardHeader
        avatar={
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" onClick  = {handleIncomingNotification}>
            <MoreVertIcon  />
          </IconButton>
        }
        title="Raviv"
        subheader="Participant"
      />

{/* Same as */}
      <CardContent>
        
        <Typography variant="body2" color="text.secondary">
       
        {/* <Box
      sx={{
        width: 300,
        height: 300,
        backgroundColor: '#bdbdbd',
       
      }}
    />   */}
            <Question />
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
