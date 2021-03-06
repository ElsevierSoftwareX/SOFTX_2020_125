//# Copyright (C) 2014-2020 Syracuse University, European Gravitational Observatory, and Christopher Newport University.  Written by Ryan Fisher and Gary Hemming. See the NOTICE file distributed with this work for additional information regarding copyright ownership.

//# This program is free software: you can redistribute it and/or modify

//# it under the terms of the GNU Affero General Public License as

//# published by the Free Software Foundation, either version 3 of the

//# License, or (at your option) any later version.

//#

//# This program is distributed in the hope that it will be useful,

//# but WITHOUT ANY WARRANTY; without even the implied warranty of

//# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

//# GNU Affero General Public License for more details.

//#

//# You should have received a copy of the GNU Affero General Public License

//# along with this program.  If not, see <http://www.gnu.org/licenses/>.
<?php
/*
This file is part of the DQSEGDB WUI.

This file was written by Gary Hemming <gary.hemming@ego-gw.it>.

DQSEGDB WUI uses the following open source software:
- jQuery JavaScript Library v1.12.4, available under the MIT licence - http://jquery.org/license - Copyright jQuery Foundation and other contributors.
- W3.CSS 2.79 by Jan Egil and Borge Refsnes.
- Font Awesome by Dave Gandy - http://fontawesome.io.
- Jquery Timepicker, developed and maintained by Willington Vega. Code licensed under the MIT and GPL licenses - http://timepicker.co
*/

// Get libraries.
require_once 'Constants.php';
require_once 'DAO.php';

// Session Manager class.
class SessionManager {

	/* Constructor. */
	public function __construct() {
		// Set sessions.
		$this->set_sessions();
	}
	
	/* Set sessions. */	
	public function set_sessions() {
		// Instantiate.
		$constants = new Constants();
		$dao = new DAO();
		// Host ID.
		if(!isset($_SESSION['host_id'])) {
		    // Get an array of details for the default host.
		    $a = $dao->get_host_details($dao->get_default_host());
			// Set to zero, thus requiring authentication.
		    $_SESSION['host_id'] = $a[0]['host_id'];
		}
		// IFO.
		if(!isset($_SESSION['ifo'])) {
		    $_SESSION['ifo'] = NULL;
		}
		// De-selected IFOs.
		if(!isset($_SESSION['deselected_ifo'])) {
		    $_SESSION['deselected_ifo'] = array();
		}
		// DQ Flag.
		if(!isset($_SESSION['dq_flag_uris'])) {
		    $_SESSION['dq_flag_uris'] = array();
		}
		// Flag filter.
		if(!isset($_SESSION['flag_filter'])) {
		    $_SESSION['flag_filter'] = NULL;
		}
		// GPS start.
		if(!isset($_SESSION['gps_start'])) {
		    $_SESSION['gps_start'] = '';
		}
		// GPS stop.
		if(!isset($_SESSION['gps_stop'])) {
		    $_SESSION['gps_stop'] = '';
		}
		// Include history.
		if(!isset($_SESSION['include_history'])) {
		    $_SESSION['include_history'] = $constants->include_history_default;
		}
		// Output format.
		if(!isset($_SESSION['output_format'])) {
		    $_SESSION['output_format'] = $dao->get_default_output_format();
		}
		// Choose-flag option.
		if(!isset($_SESSION['choose_flag_option'])) {
		    $_SESSION['choose_flag_option'] = $constants->choose_flag_option_default;
		}
	}

}

?>