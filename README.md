# Haven 3.0 Tokenomics Proposal Playground
Run simulations with this Streamlit App
- [Repo](https://github.com/Reed-Schimmel/haven-vbs-streamlit)
- [Web App](https://vbs-simulator.streamlit.app/)

## Haven Blog Posts
- [Haven 3.0 Tokenomics Proposal (light)](https://havenprotocol.org/2022/10/03/haven-3-0-tokenomics-proposal-light/)
- [Haven 3.0 Tokenomics Proposal (full)](https://havenprotocol.org/2022/10/02/haven-3-0-tokenomics-proposal/)

<!-- # TODOs
-TODO: add `pip install -e .` somewhere
- update deps https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/app-dependencies
- update cloud pointed file https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app
- Must I `pip install -e .` before each test? -->

## Setup (Using Anaconda)
1. `conda create -n vbs_streamlit python=3.10`
1. `conda activate vbs_streamlit`
1. `pip install -r requirements.txt`
1. `pip install -e .`

- To run the app: `streamlit run streamlit_app.py`
<!-- - To run the tests: `pytest` -->


# Useful Documentation
- https://docs.streamlit.io/knowledge-base/using-streamlit/how-do-i-run-my-streamlit-script
- https://github.com/GokuMohandas/mlops-course

# Future Ideas:
- Fetch XHV price via https://github.com/man-c/pycoingecko
- benchmark caching to see if it helps or hurts

# Donations:
*VBS Simulator* is developed\* and maintained by the volunteer efforts of [Reed Schimmel](https://github.com/Reed-Schimmel).
- Haven: hvxyCn1Umq3PuQ7pWzixJnFtZNeDTfy8tQE3DjKLZ8pt8gvcqP9A3UCi6PizS2d19dZkdNMVzsPxhLoYSkLdDQLd8Xqbrrn3PX
- Monero: 87L9AVmqrPATUCJnHrJkPBZGM27qN5BxY7uwDJQ6XSCw4VRtYFY5Lpw2Rt9ZxU5nFiev9hvyP4pbD8RD4EMQh9d9H9LNaUA

\* In collaboration with **Community Manager
Contributor [xKleinroy](https://havenprotocol.org/team/)**, who generously provided pseudocode and quality assurance.