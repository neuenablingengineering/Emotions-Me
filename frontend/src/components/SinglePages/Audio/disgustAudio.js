import React, { Component } from 'react'
import AudioPlayer from 'react-playlist-player'
import emojis from "../../../constants/Emojis";
import Link from "react-router-dom/es/Link";

export  class disgustAudioPlayer extends Component {
    state = {
        currentPlayList: {},
        songs: [
            {
                position: '1',
                songName: 'Very Disgusted - "It\'s 11 o\'clock"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IEO_DIS_VE.wav'
            },
            {
                position: '2',
                songName: 'Very Disgusted - "I would like a new alarm clock"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IWL_DIS_VE.wav'
            },
            {
                position: '3',
                songName: 'Very Disgusted - "The surface is slick"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/TSI_DIS_VE.wav'
            },
            {
                position: '4',
                songName: 'Very Disgusted - "I\'m on my way to the meeting"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IOM_DIS_VE.wav'
            },
            {
                position: '5',
                songName: 'Very Disgusted - "I think I have a doctor\'s appointment"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/ITH_DIS_VE.wav'
            },
            {
                position: '6',
                songName: 'Very Disgusted - "The airplane is almost full"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/TAI_DIS_VE.wav'
            },
            {
                position: '7',
                songName: 'Somewhat Disgusted - "It\'s 11 o\'clock" 1',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IEO_DIS_SO1.wav'
            },
            {
                position: '8',
                songName: 'Somewhat Disgusted - "I wonder what this is about"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IWW_DIS_SO.wav'
            },
            {
                position: '9',
                songName: 'Somewhat Disgusted - "We\'ll stop in a couple of minutes"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/WSI_DIS_SO.wav'
            },
            {
                position: '10',
                songName: 'Somewhat Disgusted - "It\'s 11 o\'clock" 2',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IEO_DIS_SO2.wav'
            },
            {
                position: '11',
                songName: 'Somewhat Disgusted - "I\'m on my way to the meeting"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IOM_DIS_SO.wav'
            },
            {
                position: '12',
                songName: 'Somewhat Disgusted - "The airplane is almost full"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/TAI_DIS_SO.wav'
            },
            {
                position: '13',
                songName: 'A Little Disgusted - "It\'s 11 o\'clock"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/IEO_DIS_LI.wav'
            },
            {
                position: '14',
                songName: 'A Little Disgusted - "Don\'t forget a jacket"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/DFA_DIS_LI.wav'
            },
            {
                position: '15',
                songName: 'A Little Disgusted - "That is exactly what happened"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/TIE_DIS_LI.wav'
            },
            {
                position: '16',
                songName: 'A Little Disgusted - "I think I\'ve seen this before"',
                songUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Audio/Disgust/ITS_DIS_LI.wav'
            }
        ],
    };

    loadPlayList = () =>
        this.setState({
            currentPlayList: {
                playlistCoverUrl: 'https://s3.amazonaws.com/emotions-and-me-bucket/Photos/Disgust/1.jpg',
                playlistName: 'Disgust Playlist',
                songs: this.state.songs,
                type: 'album'
            }
        });

    returnToTasklist = () => {
        if (this.props.location.state !== undefined) {
            if (this.props.location.state.isTLTask === true) {
                return (
                    <div className="w3-display-container">
                        <Link to={{
                            pathname: '/tasklistpage',
                            state: {
                                tasklistName: this.props.location.state.tasklistName,
                                tasklistData: this.props.location.state.tasklistData
                            }
                        }} style={{textDecoration: 'none'}}>
                            <button className="w3-button w3-theme w3-display-right w3-margin-bottom">
                                Return to Tasklist <i className="arrow right"/>
                            </button>
                        </Link>
                    </div>
                )
            }
        }
        return <div className="w3-display-container"/>
    };

    render() {
        return (
            <div className="w3-container">
                <h1 className="w3-center">
                    <img className="w3-image w3-margin-right" src={emojis.disgust} alt="disgust" style={{width: '8%'}}/>
                    Disgust Audio Clips
                    <img className="w3-image w3-margin-left" src={emojis.disgust} alt="disgust" style={{width: '8%'}}/>
                </h1>
                <div className="audio-clips w3-center">
                    <div className="play-all w3-margin">
                        <button className="w3-button w3-theme w3-padding-large" onClick={this.loadPlayList}>
                            Play All
                        </button>
                        <AudioPlayer currentPlayList={this.state.currentPlayList}
                                     onToggle={({audioPlaying}) => console.log({audioPlaying})}/>
                    </div>
                    {this.state.songs.map((song, i) => {
                        return (
                            <div className="songs w3-margin" key={i}>
                                <div className="w3-center">
                                    <label className="w3-padding">{song.songName}</label>
                                    <div>
                                        <audio controls>
                                            <source src={song.songUrl} type="audio/wav" id={song.songName}/>
                                            Your browser does not support the audio element.
                                        </audio>
                                    </div>
                                </div>
                            </div>
                        )
                    })}
                </div>
                <div className="w3-display-container">
                    <a href="/audiolist">
                        <button className="w3-button w3-theme w3-display-left w3-margin-bottom">
                            <i className="arrow left"/> Back
                        </button>
                    </a>
                </div>
                {this.returnToTasklist()}
            </div>
        )
    }
}
