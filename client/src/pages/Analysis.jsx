import React, { useState, useContext } from 'react';
import TrendChart from '../graphing/TrendChart';
import {useOutletContext} from "react-router-dom";
import { prepareDataForPlot } from '../graphing/dataProcessing';
import GraphOptions from '../graphing/GraphOptions';
import styled from 'styled-components';
import Loading from './Loading'
import AnalysisHoney from '../graphing/AnalysisHoney';
import AnalysisHealth from '../graphing/AnalysisHealth';
import { Button, HexagonButton } from '../MiscStyling';
import { UserContext } from '../context/userProvider';

const ButtonContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 50px;
`

const Analysis = () => {
    const { user } = useContext(UserContext);
    const { graphData, graphDataUser } = useOutletContext();
    const [activeTab, setActiveTab] = useState('healthAll');

    if (graphData.length===0) return <Loading />

    return (
        <main>
            <h1>Hive Analysis</h1>
            <ButtonContainer>
                {user && <HexagonButton isActive={activeTab==='honeyUser'} onClick={()=>setActiveTab('honeyUser')}>My Honey</HexagonButton>}
                {user && <HexagonButton isActive={activeTab==='healthUser'} onClick={()=>setActiveTab('healthUser')}>Hive Health</HexagonButton>}                
                <HexagonButton isActive={activeTab==='honeyAll'} onClick={()=>setActiveTab('honeyAll')}>Honey Trends</HexagonButton>
                <HexagonButton isActive={activeTab==='healthAll'} onClick={()=>setActiveTab('healthAll')}>Health Trends</HexagonButton>
            </ButtonContainer>
            {activeTab==='honeyUser' &&
                <AnalysisHoney
                    graphData={graphDataUser.aggregated}
                    label='My Honey Statistics'
                />
            }
            {activeTab==='healthUser' &&
                <AnalysisHealth
                    graphData={graphDataUser.normalized}
                    label='My Hive Statistics'
                />
            }
            {activeTab==='honeyAll' &&
                <AnalysisHoney
                    graphData={graphData.aggregated}
                    label='Honey Statistics for All Users'
                />
            }
            {activeTab==='healthAll' &&
                <AnalysisHealth
                    graphData={graphData.normalized}
                    label='Hive Statistics for All Users'
                />
            }
        </main>
    );
}

export default Analysis;
