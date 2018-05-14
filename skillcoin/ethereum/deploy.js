const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3 = require('web3')
const compileFactory = require('./build/SkillToken.json');

const MNEMONIC = 'hold chicken doll strategy flip vibrant swing antique doctor brief merit airport';
const RINKEBY = 'https://rinkeby.infura.io/zgQC1j3K0CuHfKyRukAz';

const provider = new HDWalletProvider(
    MNEMONIC,
    RINKEBY
);
const web3 = new Web3(provider);

const deploy = async () => {
    const accounts = await web3.eth.getAccounts();
    const data = '0x' + compileFactory.bytecode;
    console.log('Attemping to deploy from account', accounts[0]);
    const contract = await new web3.eth.Contract(JSON.parse(compileFactory.interface))
        .deploy({ data: data })
        .send({
            from: accounts[0],
            gas: '5000000'
        });
    
    console.log('Contract deployed to:', contract.options.address);
    console.log('Please go to this link to see the contract: https://rinkeby.etherscan.io/address/%s', contract.options.address);
    console.log('Then go to https://rinkeby.etherscan.io/verifyContract2?a=%s to verify and publish the contract', contract.options.address);
}

deploy();
