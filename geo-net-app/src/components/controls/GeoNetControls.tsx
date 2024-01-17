import {Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Box} from "@chakra-ui/react";
import MapControls from "./MapControls.tsx";

function GeoNetControls({settings, handleSettingsChange, resetNodeSelection}) {
    return (
        <Box position="absolute" top={1} right={1}>
            <Accordion allowToggle>
                <AccordionItem>
                    <AccordionButton>
                        <Box flex="1" textAlign="left">
                            Map Controls
                        </Box>
                        <AccordionIcon/>
                    </AccordionButton>
                    <AccordionPanel>
                        <MapControls settings={settings} onChange={handleSettingsChange} onResetNodeSelection={resetNodeSelection}/>
                    </AccordionPanel>
                </AccordionItem>
            </Accordion>
        </Box>
    )
}

export default GeoNetControls;