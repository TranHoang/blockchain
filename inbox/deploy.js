const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3 = require('web3')
const { interface, bytecode } = require('./compile');

const MNEMONIC = 'hold chicken doll strategy flip vibrant swing antique doctor brief merit airport';
const RINKEBY = 'https://rinkeby.infura.io/zgQC1j3K0CuHfKyRukAz';

const provider = new HDWalletProvider(
    MNEMONIC,
    RINKEBY
);
const web3 = new Web3(provider);

const deploy = async () => {
    const accounts = await web3.eth.getAccounts();
    const data = '0x' + bytecode;
    console.log('Attemping to deploy from account', accounts[0]);
    const contract = await new web3.eth.Contract(JSON.parse(interface))
        .deploy({
            data: data,
            arguments: ['Hi there!']
        })
        .send({
            from: accounts[0],
            gas: '1000000'
        });

    console.log('Contract deployed to', contract.options.address);
}

deploy();


// Contract deployed list
// 0xF47Ae3b626E5ac03B76Ab5270B0976553E9E25f2