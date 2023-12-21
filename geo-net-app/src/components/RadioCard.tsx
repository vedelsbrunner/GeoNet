import {Box, useRadio,} from '@chakra-ui/react';

export function RadioCard(props) {
    const {getInputProps, getCheckboxProps} = useRadio(props);
    const input = getInputProps();
    const checkbox = getCheckboxProps();

    return (
        <Box as='label'>
            <input {...input} />
            <Box
                {...checkbox}
                cursor='pointer'
                borderWidth='1px'
                borderRadius='md'
                boxShadow='md'
                _checked={{
                    bg: 'teal.600',
                    color: 'white',
                    borderColor: 'teal.600',
                }}
                _focus={{
                    boxShadow: 'outline',
                }}
                p={5}
                textAlign='center'
                transition='all 0.2s cubic-bezier(.08,.52,.52,1)'
                _hover={{
                    boxShadow: 'lg',
                }}
            >
                {props.children}
            </Box>
        </Box>
    );
}